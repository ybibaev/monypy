import weakref

DEFAULT_MANAGER_CLASS_NAME = 'Manager'


class BaseManager:
    def __init__(self, collection):
        self.__collection = collection

    def __getattr__(self, item):
        return getattr(self.__collection, item)

    @classmethod
    def for_doc(cls, doc_class):
        from .doc import DocBase

        assert issubclass(doc_class, DocBase)

        manager_class_name = f'{doc_class.__name__}{DEFAULT_MANAGER_CLASS_NAME}'
        return type(manager_class_name, (cls,), {
            '__doc_class': weakref.ref(doc_class),
        })

    @property
    def _doc_class(self):
        ref = getattr(self, '__doc_class')
        return ref()


class Manager(BaseManager):
    async def create(self, **kwargs):
        obj = self._doc_class(**kwargs)
        await obj.save()
        return obj


class ManagerDescriptor:
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        if instance is not None:
            raise AttributeError(f'Instance of {owner.__name__!r} has no attribute "manager"')

        return self.manager
