import pytest

from monypy import Doc, Manager


@pytest.mark.asyncio
async def test_get_manger_from_instance(empty_doc):
    empty = empty_doc()

    with pytest.raises(AttributeError):
        await empty.manager.count()


@pytest.mark.asyncio
async def test_get_manger_from_class(empty_doc):
    assert 0 == await empty_doc.manager.count_documents({})


@pytest.mark.asyncio
async def test_custom_manager_method(settings):
    class EmptyDocManager(Manager):
        async def count_emtpy(self):
            return await self.count_documents({'empty': True})

    class EmptyDoc(settings, Doc):
        manager_class = EmptyDocManager

        __init_data__ = {
            'empty': True,
        }

    await EmptyDoc().save()
    await EmptyDoc(empty=False).save()

    try:
        assert await EmptyDoc.manager.count_documents({}) == 2
        assert await EmptyDoc.manager.count_emtpy() == 1

    finally:
        await EmptyDoc.manager.drop()


@pytest.mark.asyncio
async def test_manager_create(empty_doc):
    assert await empty_doc.manager.count_documents({}) == 0
    obj = await empty_doc.manager.create(test='test')

    assert await empty_doc.manager.count_documents({}) == 1
    assert obj is not None
    assert 'test' in obj
    assert '_id' in obj
