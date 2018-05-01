import pytest


@pytest.mark.asyncio
async def test_get_manger_from_instance(empty_doc):
    empty = empty_doc()

    with pytest.raises(AttributeError):
        await empty.manager.count()


@pytest.mark.asyncio
async def test_get_manger_from_class(empty_doc):
    assert 0 == await empty_doc.manager.count()
