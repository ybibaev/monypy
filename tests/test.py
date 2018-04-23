import pytest

from monypy.base import Doc


@pytest.mark.asyncio
async def test_doc(event_loop):
    class MyDoc(Doc):
        __init_data__ = {
            'x': 'x',
            'y': 'y'
        }

        __doc__meta__ = {
            'test': 'test'
        }

    d = MyDoc(x='xx')

    assert d.x == 'xx'
    assert d.y == 'y'
