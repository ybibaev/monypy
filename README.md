# monypy - asynchronous lightweight ODM for MongoDB 

[![Build Status](https://travis-ci.org/nede1/monypy.svg?branch=master)](https://travis-ci.org/nede1/monypy)

### Dependencies
```
python >= 3.6
motor >= 1.2.0
```

### Installation
```bash
pipenv install git+https://github.com/nede1/monypy#egg=monypy
```

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

assert not callable(user.instance_id)
assert user.instance_id == id(user)

```