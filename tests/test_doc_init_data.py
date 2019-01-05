import pytest

from monypy import Doc


@pytest.mark.asyncio
async def test_init_data_as_dict(empty_doc):
    with pytest.raises(TypeError):
        empty_doc({'test_1': 'test_1', 'test': 'test_2'})


@pytest.mark.asyncio
async def test_init_data_as_kwargs(empty_doc):
    empty = empty_doc(**{'test_1': 'test_1', 'test': 'test_2'})

    assert empty['test_1'] == 'test_1'
    assert empty['test'] == 'test_2'


@pytest.mark.asyncio
async def test_init_data_as_dict_and_kwargs(empty_doc):
    with pytest.raises(TypeError):
        empty_doc({'test_1': 'test_1', 'test': 'test_2'}, x=45)


@pytest.mark.asyncio
async def test_init_data_change(empty_doc):
    empty = empty_doc(id=12345)

    empty.id = 666

    await empty.save()
    await empty.refresh()

    assert empty.id == 666


@pytest.mark.asyncio
async def test_init_data_with_callable(settings):
    def foo(instance):
        return id(instance)

    class EmptyDoc(settings, Doc):
        __init_data__ = {
            'test': foo,
        }

    empty = EmptyDoc()

    assert isinstance(empty['test'], int)


@pytest.mark.asyncio
async def test_init_data_with_callable_kwargs(empty_doc):
    def foo(instance):
        return id(instance)

    empty = empty_doc(test=foo)
    assert callable(empty['test'])


@pytest.mark.asyncio
async def test_init_data_save_and_refresh_nested(settings):
    class EmptyDoc(settings, Doc):
        __init_data__ = {
            'test': 'test'
        }

    empty = EmptyDoc(**{'test2': {'test2': 'test2'}})
    await empty.save()
    await empty.refresh()

    assert 'test' not in empty['test2']


@pytest.mark.asyncio
async def test_init_data_in_class_definition(settings):
    class EmptyDoc(settings, Doc):
        __init_data__ = {
            'test': 'test'
        }

    empty = EmptyDoc()
    assert empty.test == 'test'


@pytest.mark.asyncio
async def test_init_data_in_class_and_kwargs(settings):
    class EmptyDoc(settings, Doc):
        __init_data__ = {
            'test': 'test'
        }

    empty = EmptyDoc(test='test_45')
    assert empty.test == 'test_45'


@pytest.mark.asyncio
async def test_init_data_in_class_inheritance(settings):
    class InitData:
        __init_data__ = {
            'test': 'test'
        }

    class EmptyDoc(settings, InitData, Doc):
        pass

    empty = EmptyDoc()

    assert empty.test == 'test'
