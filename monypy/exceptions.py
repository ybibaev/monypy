class BaseMonypyException(Exception):
    pass


class DocumentDoesNotExistError(BaseMonypyException):
    pass


class DocumentInitDataError(BaseMonypyException):
    pass
