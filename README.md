# monypy - asynchronous lightweight ODM for MongoDB 

[![Build Status](https://travis-ci.org/nede1/monypy.svg?branch=master)](https://travis-ci.org/nede1/monypy)

## Dependencies ##
```
python >= 3.6
motor >= 1.2.0
```

## Installation ##
```bash
pipenv install git+https://github.com/nede1/monypy#egg=monypy
```

## Quick Start ##
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
    
user = User({'name': 'John'})

assert '_id' not in user
assert user.name == 'John'
assert user.sex == 'male'

assert not callable(user.instance_id)
assert user.instance_id == id(user)

asyncio.get_event_loop() \
    .run_until_complete(user.save())

assert '_id' in user
```

## API Reference ##

### Doc ###
* #### `__database__` ####
    Description
    
* #### `__collection__` ####
    Description

* #### `__abstract__` ####
    Description

* #### `__loop__` ####
    Description

* #### `__init_data__` ####
  Description

* #### `manager` ####
    Description

* #### `_as_dict()` ####
    Returns the object as a __dict__.
    
* #### `save()` ####
    __сoroutine__. Saves the object in the database if it does not exist, if it exists, it updates.

* #### `delete()` ####
    __сoroutine__. Removes an object from the database. If the object does not exist, then the __DocumentDoesNotExistError__ exception is raised.

* #### `refresh()` ####
    __сoroutine__. Updates an object from the database. If the object does not exist, then the __DocumentDoesNotExistError__ exception is raised.

### Manager ###
