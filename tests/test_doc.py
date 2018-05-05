import pytest


@pytest.mark.asyncio
async def test_setattr(empty_doc):
    empty = empty_doc()

    empty.test = 'test'
    assert empty.test == 'test'


@pytest.mark.asyncio
async def test_getattr(empty_doc):
    empty = empty_doc(test='test')

    assert empty.test == 'test'


@pytest.mark.asyncio
async def test_getattr_without_data(empty_doc):
    empty = empty_doc()

    with pytest.raises(AttributeError):
        test = empty.test  # noqa


@pytest.mark.asyncio
async def test_delattr(empty_doc):
    empty = empty_doc(test='test')

    del empty.test

    assert 'test' not in empty


@pytest.mark.asyncio
async def test_delattr_without_data(empty_doc):
    empty = empty_doc()

    with pytest.raises(AttributeError):
        del empty.test


@pytest.mark.asyncio
async def test_repr(empty_doc):
    empty = empty_doc(test='test')

    assert "<EmptyDoc({'test': 'test'})>" in repr(empty)
