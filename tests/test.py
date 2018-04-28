import pytest

from monypy import Doc
from monypy.doc import ALL_MONGO_KEYS


@pytest.mark.asyncio
async def test_doc(event_loop):
    class User(Doc):
        __init_data__ = {
            'sex': 'male'
        }

        __database__ = {
            'host': 'localhost',
            'port': 27017,
            'name': 'my_test_base'
        }

        __loop__ = event_loop

    user = User({'name': 'Vasya'})

    await user.save()

    assert '_id' in user
    assert user.name == 'Vasya'
    assert user.sex == 'male'

    id_ = user._id
    await user.save()
    assert id_ == user._id

    t = await User.manager.find_one({'_id': user._id})

    for k in ALL_MONGO_KEYS:
        assert k not in t

    await t.save()

    tt = await User.manager.find_one({'_id': user._id})

    for k in ALL_MONGO_KEYS:
        assert k not in tt
