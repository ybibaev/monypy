from bson.codec_options import DEFAULT_CODEC_OPTIONS

from .connection import connect
from .manager import Manager

DOC_DATA = '#data'

DOC_DATABASE = '__database__'
DOC_LOOP = '__loop__'


class DocMeta(type):
    def __new__(mcs, name, bases, clsargs):
        database = None
        loop = None

        if DOC_DATABASE in clsargs:
            database = clsargs.pop(DOC_DATABASE)
            loop = clsargs.pop(DOC_LOOP, None)

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

            manager = Manager(collection)
            cls.manager = ManagerDescriptor(manager)

        return cls


class ManagerDescriptor:
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        if instance:
            raise AttributeError('Instance do not have manger')

        return self.manager
