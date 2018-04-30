import pytest

from monypy import Doc
from monypy.meta import DOC_DATA


@pytest.mark.asyncio
async def test_doc(event_loop):  # TODO: move to separate tests
    class User(Doc):
        __init_data__ = {
            'sex': 'male'
        }

        __database__ = {
            'host': 'localhost',
            'port': 27017,
            'name': 'my_test_base',
            'collection': 'test_collection'
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

    await user.delete()
    assert '_id' not in user

    petya = User(name='Petya')
    await petya.save()

    assert petya.name != user.name

    await user.save()

    assert 'test' not in user
    user.test = 'test'

    assert user.test == 'test'

    await user.refresh()

    assert 'test' not in user

    assert '<User({' in repr(user)

    assert user.__dict__[DOC_DATA] is not user.as_dict()
