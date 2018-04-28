class Manager:
    def __init__(self, collection):
        self.__collection = collection

    def __getattr__(self, item):
        return getattr(self.__collection, item)
