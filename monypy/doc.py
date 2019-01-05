import abc
import reprlib
from collections import MutableMapping

from .exceptions import DocumentDoesNotExist
from .meta import DocMeta, DOC_DATA

MONGODB_ID_KEY = '_id'


class DocBase(MutableMapping, metaclass=DocMeta):
    __init_data__ = None

    __collection__ = None
    __database__ = None

    __abstract__ = False

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def __getattr__(self, item):
        pass

    @abc.abstractmethod
    def __setattr__(self, key, value):
        pass

    @abc.abstractmethod
    def __delattr__(self, item):
        pass

    @abc.abstractmethod
    def __contains__(self, item):
        pass

    @abc.abstractmethod
    async def save(self) -> None:
        pass

    @abc.abstractmethod
    async def refresh(self) -> None:
        pass

    @abc.abstractmethod
    async def delete(self) -> None:
        pass

    def __repr__(self):
        name = type(self).__name__
        repr_ = reprlib.repr(vars(self)[DOC_DATA])
        return f'<{name}({repr_})>'

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return vars(self)[DOC_DATA] == vars(other)[DOC_DATA]


class Doc(DocBase):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f'{type(self).__name__!r} object has no attribute {key!r}')

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f'{type(self).__name__!r} object has no attribute {key!r}')

    def __getitem__(self, item):
        return vars(self)[DOC_DATA][item]

    def __setitem__(self, key, value):
        if key in self.__init_data__:
            del self.__init_data__[key]

        if type(value) is type(self):
            value_data = vars(value)[DOC_DATA].copy()
            for _key in value.__init_data__:
                del value_data[_key]

            value = value_data

        vars(self)[DOC_DATA][key] = value

    def __delitem__(self, key):
        del vars(self)[DOC_DATA][key]

    def __contains__(self, item):
        return item in vars(self)[DOC_DATA]

    def __len__(self):
        return len(vars(self)[DOC_DATA])

    def __iter__(self):
        return iter(vars(self)[DOC_DATA])

    async def save(self):
        if MONGODB_ID_KEY not in self:
            result = await type(self).documents.insert_one(vars(self)[DOC_DATA])
            vars(self)[DOC_DATA][MONGODB_ID_KEY] = result.inserted_id
        else:
            await type(self).documents.replace_one({MONGODB_ID_KEY: self._id}, vars(self)[DOC_DATA])

    async def delete(self):
        if MONGODB_ID_KEY not in self:
            raise DocumentDoesNotExist

        await type(self).documents.delete_one({MONGODB_ID_KEY: self._id})
        del self._id

    async def refresh(self):
        if MONGODB_ID_KEY not in self:
            raise DocumentDoesNotExist

        result = await type(self).documents.find_one({MONGODB_ID_KEY: self._id})
        vars(self)[DOC_DATA] = vars(result)[DOC_DATA]
