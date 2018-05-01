import pytest

from monypy import Doc
from monypy.meta import DOC_DATA


@pytest.mark.asyncio
async def test_doc(event_loop, settings):  # TODO: move to separate tests
    class User(settings, Doc):
        __init_data__ = {
            'sex': 'male'
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

    u = User({'sex': 'female', 'user_id': lambda self: 45})

    assert u.sex == 'female'
    assert u.user_id == 45
