import pytest

from monypy.doc import MONGODB_ID_KEY
from monypy.exceptions import DocumentDoesNotExist


@pytest.mark.asyncio
async def test_save(empty_doc):
    empty = empty_doc()

    assert MONGODB_ID_KEY not in empty

    await empty.save()

    assert MONGODB_ID_KEY in empty
    assert 1 == await empty_doc.documents.count({})


@pytest.mark.asyncio
async def test_save_two(empty_doc):
    empty = empty_doc()

    await empty.save()

    empty.test = 'test'
    await empty.save()

    assert MONGODB_ID_KEY in empty
    assert 1 == await empty_doc.documents.count({})


@pytest.mark.asyncio
async def test_refresh(empty_doc):
    empty = empty_doc()

    await empty.save()

    empty.test = 'test'
    await empty.refresh()

    assert MONGODB_ID_KEY in empty
    assert 'test' not in empty
    assert 1 == await empty_doc.documents.count({})


@pytest.mark.asyncio
async def test_refresh_not_saved(empty_doc):
    empty = empty_doc()

    with pytest.raises(DocumentDoesNotExist):
        await empty.refresh()

    assert MONGODB_ID_KEY not in empty


@pytest.mark.asyncio
async def test_save_nested_and_refresh(empty_doc):
    empty = empty_doc(test={'test': 'test'})

    await empty.save()
    await empty.refresh()

    assert not isinstance(empty['test'], empty_doc)


@pytest.mark.asyncio
async def test_delete(empty_doc):
    empty = empty_doc()

    await empty.save()
    await empty.delete()

    assert 0 == await empty_doc.documents.count({})


@pytest.mark.asyncio
async def test_delete_not_saved(empty_doc):
    empty = empty_doc()

    with pytest.raises(DocumentDoesNotExist):
        await empty.delete()

    assert 0 == await empty_doc.documents.count({})
