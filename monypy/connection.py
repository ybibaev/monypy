from motor.motor_asyncio import AsyncIOMotorClient

_connections = {}


def connect(**kwargs):
    io_loop = kwargs.pop('io_loop')
    key = hash(''.join(sorted(map(str, kwargs.keys()))))

    if key not in _connections:
        _connections[key] = AsyncIOMotorClient(**kwargs, io_loop=io_loop)
    return _connections[key]
