import pytest

from monypy import Doc
from monypy import connection


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

    assert "<EmptyDoc({'test': 'test'})>" == repr(empty)


@pytest.mark.asyncio
async def test_repr_too_long(empty_doc):
    empty = empty_doc(test='test-test-test-test-test-test-test-test-test-test-test-test')

    assert "<EmptyDoc({'test': 'test-test-te...est-test-test'})>" == repr(empty)


@pytest.mark.asyncio
async def test_change_collection_name(event_loop, settings):
    class EmptyDoc(settings, Doc):
        __collection__ = {
            'name': 'test_doc'
        }

    assert EmptyDoc.manager.name == 'test_doc'


@pytest.mark.asyncio
async def test_collection_name(empty_doc):
    assert empty_doc.manager.name == 'emptydoc'


@pytest.mark.asyncio
async def test_abstract_doc(settings):
    class AbstractDoc(settings, Doc):
        __abstract__ = True

    assert len(connection._connections) == 0


@pytest.mark.asyncio
async def test_inheritance_from_abstract_doc(settings):
    class AbstractDoc(settings, Doc):
        __init_data__ = {
            'test': 'test'
        }

        __abstract__ = True

    class EmptyDoc(AbstractDoc):
        pass

    assert len(connection._connections) == 1
    assert 'test' in EmptyDoc()
    assert await EmptyDoc.manager.count_documents({}) == 0


@pytest.mark.asyncio
async def test_inheritance_from_abstract_doc_two(settings):
    class AbstractDoc(Doc):
        __init_data__ = {
            'test': 'test'
        }

        __database__ = {
            'name': 'test',
            'host': 'localhost',
            'port': 27017
        }

        __abstract__ = True

    class EmptyDoc(AbstractDoc):
        pass

    assert len(connection._connections) == 1
    assert 'test' in EmptyDoc()
    assert await EmptyDoc.manager.count_documents({}) == 0


@pytest.mark.asyncio
async def test_inheritance_from_abstract_doc_twice(settings):
    class AbstractDoc(Doc):
        __init_data__ = {
            'test': 'test'
        }

        __database__ = {
            'name': 'test',
            'host': 'localhost',
            'port': 27017
        }

        __abstract__ = True

    class EmptyDoc(AbstractDoc):
        pass

    class EmptyDocTwo(AbstractDoc):
        pass

    assert len(connection._connections) == 1

    assert 'test' in EmptyDoc()
    assert 'test' in EmptyDocTwo()

    assert await EmptyDoc.manager.count_documents({}) == 0
    assert await EmptyDocTwo.manager.count_documents({}) == 0


@pytest.mark.asyncio
async def test_non_equality(empty_doc):
    doc_1 = empty_doc(name='doc_1')
    doc_2 = empty_doc(name='doc_2')

    assert doc_1 != doc_2


@pytest.mark.asyncio
async def test_equality(empty_doc):
    doc_1 = empty_doc(name='doc_1')

    assert doc_1 == doc_1
