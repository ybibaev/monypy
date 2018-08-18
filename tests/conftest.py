import pytest

from monypy import Doc
from monypy import connection


@pytest.fixture()
def settings(request):
    request.addfinalizer(connection._connections.clear)

    class DBSettings:
        __database__ = {
            'name': 'test',
            'host': 'localhost',
            'port': 27017
        }
    return DBSettings


@pytest.fixture
@pytest.mark.asyncio
async def empty_doc(settings):
    class EmptyDoc(settings, Doc):
        pass
    try:
        yield EmptyDoc

    finally:
        await EmptyDoc.manager.drop()
