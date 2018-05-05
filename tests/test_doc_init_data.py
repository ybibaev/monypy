import pytest

from monypy import Doc
from monypy.exceptions import DocumentInitDataError


@pytest.mark.asyncio
async def test_init_data_as_dict(empty_doc):
    empty = empty_doc({'test_1': 'test_1', 'test': 'test_2'})

    assert empty['test_1'] == 'test_1'
    assert empty['test'] == 'test_2'


@pytest.mark.asyncio
async def test_init_data_as_kwargs(empty_doc):
    empty = empty_doc(**{'test_1': 'test_1', 'test': 'test_2'})

    assert empty['test_1'] == 'test_1'
    assert empty['test'] == 'test_2'


@pytest.mark.asyncio
async def test_init_data_as_dict_and_kwargs(empty_doc):
    with pytest.raises(DocumentInitDataError):
        empty_doc({'test_1': 'test_1', 'test': 'test_2'}, x=45)


@pytest.mark.asyncio
async def test_init_data_change(empty_doc):
    empty = empty_doc(id=12345)

    empty.id = 666

    await empty.save()
    await empty.refresh()

    assert empty.id == 666


@pytest.mark.asyncio
async def test_init_data_with_callable(empty_doc):
    def foo(instance):
        return id(instance)

    empty = empty_doc(id=foo)
    empty_2 = empty_doc(id=foo)

    id_1 = empty['id']
    id_2 = empty_2['id']

    assert isinstance(id_1, int)
    assert isinstance(id_2, int)

    assert id_1 != id_2


@pytest.mark.asyncio
async def test_init_data_in_class_definition(event_loop, settings):
    class EmptyDoc(settings, Doc):
        __init_data__ = {
            'test': 'test'
        }

        __loop__ = event_loop

    empty = EmptyDoc()
    assert empty.test == 'test'

    await EmptyDoc.manager.drop()


@pytest.mark.asyncio
async def test_init_data_in_class_and_kwargs(event_loop, settings):
    class EmptyDoc(settings, Doc):
        __init_data__ = {
            'test': 'test'
        }

        __loop__ = event_loop

    empty = EmptyDoc(test='test_45')
    assert empty.test == 'test_45'


@pytest.mark.asyncio
async def test_init_data_in_class_inheritance(event_loop, settings):
    class InitData:
        __init_data__ = {
            'test': 'test'
        }

    class EmptyDoc(settings, InitData, Doc):
        __loop__ = event_loop

    empty = EmptyDoc()

    assert empty.test == 'test'
