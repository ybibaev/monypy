import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

_connections = {}


def connect(**kwargs):
    key = hash(''.join(sorted(map(str, kwargs.values()))))

    if key not in _connections:
        loop = asyncio.get_running_loop()
        _connections[key] = AsyncIOMotorClient(**kwargs, io_loop=loop)
    return _connections[key]
