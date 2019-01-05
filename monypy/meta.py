import abc
import copy
from collections import MutableMapping

from .exceptions import DocumentInitDataError
from .helpers import get_database, get_collection, find_token
from .manager import DEFAULT_MANAGER_OBJECT_NAME, Manager, BaseManager

DOC_DATA = '#data'

DOC_INIT_DATA = '__init_data__'
DOC_DATABASE = '__database__'
DOC_COLLECTION = '__collection__'
DOC_ABSTRACT = '__abstract__'


class DocBaseMeta(type):
    def __new__(mcs, name, bases, clsargs):
        abstract = clsargs.pop(DOC_ABSTRACT, False)
        if abstract:
            return super().__new__(mcs, name, bases, clsargs)

        database_attrs = clsargs.pop(
            DOC_DATABASE,
            find_token(bases, DOC_DATABASE)
        )
        if not database_attrs:
            return super().__new__(mcs, name, bases, clsargs)

        collection_attrs = clsargs.pop(
            DOC_COLLECTION,
            find_token(bases, DOC_COLLECTION) or {}
        )
        clsargs[DOC_INIT_DATA] = clsargs.pop(
            DOC_INIT_DATA,
            find_token(bases, DOC_INIT_DATA) or {}
        )

        cls = super().__new__(mcs, name, bases, clsargs)

        db = get_database(**database_attrs)
        collection = get_collection(cls, db, **collection_attrs)
        mcs.collect_and_setup_managers(cls, collection)

        return cls

    @staticmethod
    def collect_and_setup_managers(cls, collection):
        managers = {k: v for k, v in vars(cls).items() if isinstance(v, BaseManager)}
        if DEFAULT_MANAGER_OBJECT_NAME not in managers:
            managers[DEFAULT_MANAGER_OBJECT_NAME] = Manager()

        for manager_name, manager in managers.items():
            manager.for_doc(doc_class=cls, manager_name=manager_name, collection=collection)

    def __call__(cls, **kwargs):
        instance = super().__call__()

        init_data = {
            k: v(instance) if callable(v) else v
            for k, v in cls.get_default_init_data().items()
        }
        vars(instance)[DOC_INIT_DATA] = init_data.copy()
        vars(instance)[DOC_DATA] = init_data.copy()

        for k, v in kwargs.items():
            instance[k] = v

        return instance

    def get_default_init_data(cls) -> MutableMapping:
        default_init_data = vars(cls).get(DOC_INIT_DATA) or {}
        if not isinstance(default_init_data, MutableMapping):
            raise DocumentInitDataError('Init data must be an instance of MutableMapping')
        return copy.copy(default_init_data)


class DocMeta(DocBaseMeta, abc.ABCMeta):
    """
    Resolve metaclass's conflict
    """
    pass
