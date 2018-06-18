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
DOC_COLLECTION = '__collection__'
DOC_ABSTRACT = '__abstract__'


class DocMeta(type):
    def __new__(mcs, name, bases, clsargs):
        abstract = clsargs.pop(DOC_ABSTRACT, False)
        if abstract:
            return super().__new__(mcs, name, bases, clsargs)

        database = clsargs.pop(DOC_DATABASE, find(bases, DOC_DATABASE))
        if not database:
            return super().__new__(mcs, name, bases, clsargs)

        loop = clsargs.pop(DOC_LOOP, find(bases, DOC_LOOP))
        collection = clsargs.pop(DOC_COLLECTION, find(bases, DOC_COLLECTION))
        clsargs[DOC_INIT_DATA] = clsargs.pop(DOC_INIT_DATA, find(bases, DOC_INIT_DATA) or {})

        cls = super().__new__(mcs, name, bases, clsargs)

        db_name = database.pop('name')
        database.update(io_loop=loop)
        client = connect(**database)

        db = client[db_name]
        db_collection = create_db_collection(cls, db, collection)

        cls.manager = manager_factory(cls, db_collection)

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


def create_db_collection(doc_class, db, data):
    try:
        collection_name = data['name']
    except TypeError:
        collection_name = doc_class.__name__.lower()

    collection_codec_options = DEFAULT_CODEC_OPTIONS \
        .with_options(document_class=doc_class)

    return db[collection_name] \
        .with_options(collection_codec_options)
