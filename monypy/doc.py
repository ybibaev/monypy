import reprlib

from .exceptions import DocumentDoesNotExistError
from .manager import Manager
from .meta import DocMeta, DOC_DATA

MONGO_ID_KEY = '_id'


class DocBase(dict, metaclass=DocMeta):  # TODO: inheritance from collection.MutableMapping
    def __getitem__(self, item):
        return self.__dict__[DOC_DATA][item]

    def __setitem__(self, key, value):
        self.__dict__[DOC_DATA][key] = value

    def __delitem__(self, key):
        del self.__dict__[DOC_DATA][key]

    def __contains__(self, item):
        return item in self.__dict__[DOC_DATA]

    def __getattr__(self, key):
        try:
            return self.__dict__[DOC_DATA][key]
        except KeyError:
            raise AttributeError(f'{type(self).__name__!r} object has no attribute {key!r}')

    def __setattr__(self, key, value):
        self.__dict__[DOC_DATA][key] = value

    def __delattr__(self, key):
        try:
            del self.__dict__[DOC_DATA][key]
        except KeyError:
            raise AttributeError(f'{type(self).__name__!r} object has no attribute {key!r}')

    def __len__(self):
        return len(self.__dict__[DOC_DATA])

    def __iter__(self):
        return iter(self.__dict__[DOC_DATA])

    def _as_dict(self):
        return self.__dict__[DOC_DATA]

    def __repr__(self):
        name = type(self).__name__
        repr_ = reprlib.repr(self._as_dict())
        return f'<{name}({repr_})>'

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__dict__[DOC_DATA] == other.__dict__[DOC_DATA]

    def __ne__(self, other):
        return not self == other


class Doc(DocBase):
    manager_class = Manager

    __init_data__ = None

    __collection__ = None
    __database__ = None

    __loop__ = None

    __abstract__ = False

    async def save(self):
        if MONGO_ID_KEY not in self:
            result = await type(self).manager.insert_one(self.__dict__[DOC_DATA])
            self.__dict__[DOC_DATA][MONGO_ID_KEY] = result.inserted_id
        else:
            await type(self).manager.replace_one({MONGO_ID_KEY: self._id}, self.__dict__[DOC_DATA])

    async def delete(self):
        if MONGO_ID_KEY not in self:
            raise DocumentDoesNotExistError

        await type(self).manager.delete_one({MONGO_ID_KEY: self._id})

        del self._id

    async def refresh(self):
        if MONGO_ID_KEY not in self:
            raise DocumentDoesNotExistError

        result = await type(self).manager.find_one({MONGO_ID_KEY: self._id})
        self.__dict__[DOC_DATA] = result.__dict__[DOC_DATA]
