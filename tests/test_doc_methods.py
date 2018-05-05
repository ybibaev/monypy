import pytest

from monypy import Doc
from monypy.doc import MONGO_ID_KEY
from monypy.exceptions import DocumentDoesNotExistError
from monypy.meta import DOC_DATA


@pytest.mark.asyncio
async def test_save(empty_doc):
    empty = empty_doc()

    assert MONGO_ID_KEY not in empty

    await empty.save()

    assert MONGO_ID_KEY in empty
    assert 1 == await empty_doc.manager.count()


@pytest.mark.asyncio
async def test_save_two(empty_doc):
    empty = empty_doc()

    await empty.save()

    empty.test = 'test'
    await empty.save()

    assert MONGO_ID_KEY in empty
    assert 1 == await empty_doc.manager.count()


@pytest.mark.asyncio
async def test_refresh(empty_doc):
    empty = empty_doc()

    await empty.save()

    empty.test = 'test'
    await empty.refresh()

    assert MONGO_ID_KEY in empty
    assert 'test' not in empty
    assert 1 == await empty_doc.manager.count()


@pytest.mark.asyncio
async def test_refresh_not_saved(empty_doc):
    empty = empty_doc()

    with pytest.raises(DocumentDoesNotExistError):
        await empty.refresh()

    assert MONGO_ID_KEY not in empty


@pytest.mark.asyncio
async def test_delete(empty_doc):
    empty = empty_doc()

    await empty.save()
    await empty.delete()

    assert 0 == await empty_doc.manager.count()


@pytest.mark.asyncio
async def test_delete_not_saved(empty_doc):
    empty = empty_doc()

    with pytest.raises(DocumentDoesNotExistError):
        await empty.delete()

    assert 0 == await empty_doc.manager.count()


@pytest.mark.asyncio
async def test_as_dict(empty_doc):
    empty = empty_doc(test='test')

    d = empty.as_dict()

    assert isinstance(d, dict)
    assert not isinstance(d, Doc)
    assert empty.__dict__[DOC_DATA] is not d
