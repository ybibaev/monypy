class BaseMonypyException(Exception):
    pass


class DocumentDoesNotExist(BaseMonypyException):
    pass


class DocumentInitDataError(BaseMonypyException):
    pass
