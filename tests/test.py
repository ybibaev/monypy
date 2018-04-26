import pytest

from monypy.base import Doc


@pytest.mark.asyncio
async def test_doc(event_loop):
    class MyDoc(Doc):
        __init_data__ = {
            'x': 'x',
            'y': 'y'
        }

        __database__ = {
            'host': 'localhost',
            'port': 27017,
            'name': 'test'
        }

        __loop__ = event_loop

    d = MyDoc(x='xx')

    assert d.x == 'xx'
    assert d.y == 'y'

    await d.save()

    assert '_id' in d

    id_ = d._id

    await d.save()

    assert id_ == d._id
