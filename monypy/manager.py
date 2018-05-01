DEFAULT_MANAGER_CLASS_NAME = 'Manager'


class Manager:
    def __init__(self, collection):
        self.__collection = collection

    def __getattr__(self, item):
        return getattr(self.__collection, item)

    @classmethod
    def for_doc(cls, doc_class):
        manager_class_name = f'{doc_class.__name__}{DEFAULT_MANAGER_CLASS_NAME}'
        return type(manager_class_name, (cls,), {})


class ManagerDescriptor:
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        if instance is not None:
            raise AttributeError(f"Instance of {owner.__name__!r} has no attribute 'manager'")

        return self.manager
