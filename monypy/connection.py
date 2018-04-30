from motor.motor_asyncio import AsyncIOMotorClient

_connections = {}


def connect(host='localhost', port=27017, io_loop=None):
    if (host, port) not in _connections:
        _connections[host, port] = AsyncIOMotorClient(host=host, port=port, io_loop=io_loop)
    return _connections[host, port]
