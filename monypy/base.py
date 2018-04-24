DOC_DATA = '#data'
DOC_INIT_DATA = '__init_data__'
DOC_META = '__doc__meta__'


class DocMeta(type):
    def __new__(mcs, name, bases, clsargs):
        cls = super().__new__(mcs, name, bases, clsargs)
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
        pass

    async def delete(self):
        pass

    async def refresh(self):
        pass
