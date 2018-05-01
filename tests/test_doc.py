import pytest

from monypy import Doc
from monypy.exceptions import DocumentDoesNotExistError
from monypy.meta import DOC_DATA


@pytest.mark.asyncio
async def test_doc_like_dict(empty_doc):
    empty = empty_doc(test='test')

    assert 'test' in empty
    assert 'test_test' not in empty

    assert 1 == len(empty)

    del empty['test']

    assert 'test' not in empty

    with pytest.raises(KeyError):
        del empty['test']

    with pytest.raises(KeyError):
        test = empty['test']

    empty['test'] = 'test'
    assert 'test' in empty

    assert list(empty) == ['test']


@pytest.mark.asyncio
async def test_doc_set_get_del(empty_doc):
    empty = empty_doc()

    empty.test = 'test'
    assert empty.test == 'test'

    del empty.test

    with pytest.raises(AttributeError):
        test = empty.test

    with pytest.raises(AttributeError):
        del empty.test


@pytest.mark.asyncio
async def test_doc_methods(empty_doc):
    empty = empty_doc()

    assert 0 == await empty_doc.manager.count()
    assert '_id' not in empty

    await empty.save()
    assert 1 == await empty_doc.manager.count()
    assert '_id' in empty

    empty.test_test = 'test_test'
    assert 'test_test' in empty
    await empty.refresh()
    assert 'test_test' not in empty
    assert '_id' in empty

    await empty.delete()
    assert 0 == await empty_doc.manager.count()
    assert '_id' not in empty

    with pytest.raises(DocumentDoesNotExistError):
        await empty.refresh()

    with pytest.raises(DocumentDoesNotExistError):
        await empty.delete()


@pytest.mark.asyncio
async def test_doc(event_loop, settings):
    class User(settings, Doc):
        __init_data__ = {
            'sex': 'male'
        }

        __loop__ = event_loop

    user_1 = User({'name': 'User'})

    await user_1.save()

    assert user_1.name == 'User'
    assert user_1.sex == 'male'

    user_2 = User(name='User_2')
    await user_2.save()

    assert user_2.name != user_1.name

    assert '<User({' in repr(user_1)

    assert user_1.__dict__[DOC_DATA] is not user_1.as_dict()

    u = User({'sex': 'female', 'user_id': lambda self: 45})

    assert u.sex == 'female'
    assert u.user_id == 45
