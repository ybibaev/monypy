import pytest

from monypy import Doc
from monypy.helpers import create_motor_client, get_database


@pytest.fixture()
def settings(request, event_loop):
    class DBSettings:
        __database__ = {
            'name': 'test',
            'host': 'localhost',
            'port': 27017
        }

    def finalizer():
        async def db_cleaner():
            db = get_database(**DBSettings.__database__)
            for collection in await db.list_collection_names():
                await db.drop_collection(collection)

        event_loop.run_until_complete(db_cleaner())
        create_motor_client.cache_clear()

    request.addfinalizer(finalizer)

    return DBSettings


@pytest.fixture
@pytest.mark.asyncio
async def empty_doc(settings):
    class EmptyDoc(settings, Doc):
        pass

    return EmptyDoc
