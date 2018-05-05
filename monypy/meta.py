import copy
from contextlib import suppress

from bson.codec_options import DEFAULT_CODEC_OPTIONS

from .connection import connect
from .exceptions import DocumentInitDataError
from .manager import Manager, ManagerDescriptor

DOC_DATA = '#data'

DOC_INIT_DATA = '__init_data__'
DOC_DATABASE = '__database__'
DOC_LOOP = '__loop__'


class DocMeta(type):
    def __new__(mcs, name, bases, clsargs):
        database = clsargs.pop(DOC_DATABASE, find(bases, DOC_DATABASE))
        loop = clsargs.pop(DOC_LOOP, find(bases, DOC_LOOP))
        clsargs[DOC_INIT_DATA] = clsargs.pop(DOC_INIT_DATA, find(bases, DOC_INIT_DATA) or {})

        cls = super().__new__(mcs, name, bases, clsargs)

        if database:
            client = connect(
                host=database['host'],
                port=database['port'],
                io_loop=loop
            )

            assert 'name' in database

            base = client[database['name']]

            collection_name = database.get('collection', name.lower())
            collection_codec_options = DEFAULT_CODEC_OPTIONS.with_options(document_class=cls)
            collection = base[collection_name].with_options(collection_codec_options)

            cls.manager = manager_factory(cls, collection)

        return cls

    def __call__(cls, *args, **kwargs):
        if args and kwargs:
            raise DocumentInitDataError('Only arg or only kwargs')

        init_data = copy.deepcopy(
            args[0] if args else kwargs
        )

        if not isinstance(init_data, dict):
            raise DocumentInitDataError('Init data must be an instance of dict')

        instance = super().__call__()
        instance.__dict__[DOC_DATA] = {}

        defaults = copy.deepcopy(
            cls.__dict__.get(DOC_INIT_DATA, {})
        )

        if not isinstance(init_data, dict):
            raise DocumentInitDataError('Init data must be an instance of dict')

        defaults.update(init_data)

        for k, v in defaults.items():
            if callable(v):
                defaults[k] = v(instance)

        instance.__dict__[DOC_DATA].update(defaults)

        return instance


def manager_factory(doc_class, collection):
    manager_doc_class = doc_class.manager_class
    manager_class = (manager_doc_class.for_doc(doc_class)
                     if manager_doc_class is Manager
                     else manager_doc_class)

    manager = manager_class(collection)
    return ManagerDescriptor(manager)


def find(classes, token):
    def _find(cls):
        nonlocal token

        for c in cls.__mro__:
            target = c.__dict__.get(token)
            if target:
                return target

    with suppress(StopIteration):
        return next(filter(bool, map(_find, classes)))
