from motor.motor_asyncio import AsyncIOMotorClient


DOC_DATA = '#data'
DOC_INIT_DATA = '__init_data__'
DOC_META = '__doc__meta__'
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
            client = AsyncIOMotorClient(database['host'], database['port'], document_class=cls, io_loop=loop)
            base = client[database['name']]
            collection = base[name.lower()]
            cls._collection = collection

        return cls


class Manager:
    def __init__(self, cls):
        self.cls = cls


class DocBase(dict, metaclass=DocMeta):
    def __getitem__(self, item):
        return self.__dict__[DOC_DATA][item]

    def __setitem__(self, key, value):
        self.__dict__[DOC_DATA][key] = value

    def __delitem__(self, key):
        del self.__dict__[DOC_DATA][key]

    def __contains__(self, item):
        return item in self.__dict__[DOC_DATA]

    def __getattr__(self, item):
        return self.__dict__[DOC_DATA][item]

    def __setattr__(self, key, value):
        self.__dict__[DOC_DATA][key] = value

    def __len__(self):
        return len(self.__dict__[DOC_DATA])

    def __iter__(self):
        return iter(self.__dict__[DOC_DATA])


class Doc(DocBase):
    manager_cls = None
    _collection = None

    def __new__(cls, *args, **kwargs):
        cls.manger = (cls.manager_cls or Manager)(cls)
        init = super().__new__(cls)
        return init

    def __init__(self, *args, **kwargs):
        init_data = args[0] if args else kwargs
        defaults = getattr(self, DOC_INIT_DATA, {})
        defaults.update(init_data)
        self.__dict__[DOC_DATA] = defaults

        super().__init__()

    async def save(self):
        if '_id' not in self:
            result = await self._collection.insert_one(self.__dict__[DOC_DATA])
            self._id = result.inserted_id
        else:
            await self._collection.replace_one({'_id': self._id}, self.__dict__[DOC_DATA])

    async def delete(self):
        pass

    async def refresh(self):
        pass
