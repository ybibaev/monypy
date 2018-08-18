from .doc import Doc
from .exceptions import DocumentDoesNotExistError, DocumentInitDataError
from .manager import Manager

__version__ = '1.2dev'

__all__ = (
    'Doc',
    'Manager',
    'DocumentInitDataError',
    'DocumentDoesNotExistError',
)
