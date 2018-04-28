from motor.motor_asyncio import AsyncIOMotorClient

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
            client = AsyncIOMotorClient(
                database['host'],
                database['port'],
                document_class=cls,
                io_loop=loop
            )

            base = client[database['name']]
            collection = base[name.lower()]
            cls.manager = Manager(collection)

        return cls
