import pytest


@pytest.mark.asyncio
async def test_contains(empty_doc):
    empty = empty_doc(test='test')

    assert 'test' in empty
    assert 'test_test' not in empty


@pytest.mark.asyncio
async def test_len(empty_doc):
    empty = empty_doc(test='test')

    assert 1 == len(empty)
    del empty['test']
    assert 0 == len(empty)


@pytest.mark.asyncio
async def test_setitem(empty_doc):
    empty = empty_doc(test='test')

    empty['test_test'] = 'test_45'
    assert empty['test_test'] == 'test_45'


@pytest.mark.asyncio
async def test_delitem(empty_doc):
    empty = empty_doc(test='test')

    del empty['test']
    with pytest.raises(KeyError):
        del empty['test']


@pytest.mark.asyncio
async def test_getitem(empty_doc):
    empty = empty_doc(test='test')

    assert empty['test'] == 'test'
    with pytest.raises(KeyError):
        test = empty['test_test']  # noqa


@pytest.mark.asyncio
async def test_iter(empty_doc):
    empty = empty_doc(test='test')

    assert list(empty) == ['test']
