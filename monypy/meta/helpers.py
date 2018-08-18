from contextlib import suppress
from itertools import chain

from bson.codec_options import DEFAULT_CODEC_OPTIONS

from ..connection import connect
from ..manager import Manager, ManagerDescriptor


def get_database(**database_attrs):
    attrs = dict(database_attrs)
    db_name = attrs.pop('name')
    client = connect(**attrs)
    return client[db_name]


def get_collection(doc_class, db, data):
    try:
        collection_name = data['name']
    except TypeError:
        collection_name = doc_class.__name__.lower()

    collection_codec_options = (DEFAULT_CODEC_OPTIONS
                                .with_options(document_class=doc_class))

    return (db[collection_name]
            .with_options(collection_codec_options))


def manager_factory(doc_class, collection):
    manager_doc_class = doc_class.manager_class
    manager_class = (manager_doc_class.for_doc(doc_class)
                     if manager_doc_class is Manager
                     else manager_doc_class)

    manager = manager_class(collection)
    return ManagerDescriptor(manager)


def find_token(classes, token):
    def find(cls):
        targets = (c.__dict__.get(token) for c in cls.__mro__)
        return filter(None, targets)

    with suppress(StopIteration):
        return next(chain.from_iterable(map(find, classes)))
