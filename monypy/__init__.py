from .doc import Doc
from .exceptions import DocumentDoesNotExist, DocumentInitDataError
from .manager import Manager

__version__ = '2.0.1'

__all__ = (
    'Doc',
    'Manager',
    'DocumentInitDataError',
    'DocumentDoesNotExist',
)
