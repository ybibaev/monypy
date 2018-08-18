import pytest

from monypy import Doc
from monypy.meta.helpers import create_motor_client


@pytest.fixture()
def settings(request):
    request.addfinalizer(create_motor_client.cache_clear)

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
