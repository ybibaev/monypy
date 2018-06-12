import pytest

from monypy import Doc, Manager


@pytest.mark.asyncio
async def test_get_manger_from_instance(empty_doc):
    empty = empty_doc()

    with pytest.raises(AttributeError):
        await empty.manager.count()


@pytest.mark.asyncio
async def test_get_manger_from_class(empty_doc):
    assert 0 == await empty_doc.manager.count()


@pytest.mark.asyncio
async def test_custom_manager_method(event_loop, settings):
    class EmptyDocManager(Manager):
        def get_empty(self):
            return self.find({'empty': True})

    class EmptyDoc(settings, Doc):
        manager_class = EmptyDocManager

        __init_data__ = {
            'empty': True,
        }

        __loop__ = event_loop

    await EmptyDoc().save()
    await EmptyDoc(empty=False).save()

    try:
        assert await EmptyDoc.manager.count() == 2
        assert await EmptyDoc.manager.get_empty().count() == 1

    finally:
        await EmptyDoc.manager.drop()
