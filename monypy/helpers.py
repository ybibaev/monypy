from contextlib import suppress
from functools import lru_cache
from itertools import chain

from bson.codec_options import DEFAULT_CODEC_OPTIONS
from motor.motor_asyncio import AsyncIOMotorClient


def get_database(**database_attrs):
    attrs = dict(database_attrs)
    db_name = attrs.pop('name')
    client = create_motor_client(**attrs)
    return client[db_name]


@lru_cache(typed=True)
def create_motor_client(**kwargs):
    return AsyncIOMotorClient(**kwargs)


def get_collection(doc_class, db, **options):
    collection_name = options.get('name') or doc_class.__name__.lower()
    collection_codec_options = (DEFAULT_CODEC_OPTIONS
                                .with_options(document_class=doc_class))

    return (db[collection_name]
            .with_options(collection_codec_options))


def find_token(classes, token):
    def find(cls):
        targets = (vars(c).get(token) for c in cls.__mro__)
        return filter(None, targets)

    with suppress(StopIteration):
        return next(chain.from_iterable(map(find, classes)))
