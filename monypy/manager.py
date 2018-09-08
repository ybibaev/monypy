from typing import Any

DEFAULT_MANAGER_CLASS_NAME = 'Manager'
DEFAULT_MANAGER_OBJECT_NAME = 'documents'


class BaseManager:
    def __init__(self):
        self._doc_class = self._collection = None

    def __getattr__(self, item: str) -> Any:
        return getattr(self._collection, item)

    def for_doc(self, doc_class, collection, manager_name: str) -> None:
        self._collection = collection
        self._doc_class = doc_class
        setattr(doc_class, manager_name, ManagerDescriptor(self))


class Manager(BaseManager):
    async def create(self, **kwargs):
        obj = self._doc_class(**kwargs)
        await obj.save()
        return obj

    def count(self, filter, session=None, **kwargs):
        """
        Method-alias on count_documents
        """
        return self.count_documents(filter, session=session, **kwargs)


class ManagerDescriptor:
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        if instance is not None:
            raise AttributeError(f'Instance of {owner.__name__!r} has no attribute "manager"')

        return self.manager
