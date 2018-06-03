from .doc import Doc
from .exceptions import DocumentDoesNotExistError, DocumentInitDataError
from .manager import Manager

__version__ = '0.9.2'

__all__ = (
    'Doc',
    'Manager',
    'DocumentInitDataError',
    'DocumentDoesNotExistError',
)
