# monypy
#### async lightweight ODM for mongodb

[![Build Status](https://travis-ci.org/nede1/monypy.svg?branch=master)](https://travis-ci.org/nede1/monypy)

### Example:
```python
import asyncio
from monypy import Doc


class User(Doc):
    __init_data__ = {
        'sex': 'male',
        'instance_id': lambda i: id(i)
    }
    
    __database__ = {
        'name': 'test',
        'host': 'localhost',
        'port': 27017
    }
    
user = User({'name': 'Vasya'})

asyncio.get_event_loop() \
    .run_until_complete(user.save())


assert '_id' in user
assert user.name == 'Vasya'
assert user.sex == 'male'

```