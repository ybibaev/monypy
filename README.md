# monypy - asynchronous lightweight ODM for MongoDB 

[![Build Status](https://travis-ci.org/nede1/monypy.svg?branch=master)](https://travis-ci.org/nede1/monypy)

## Dependencies ##
```
python >= 3.6
motor >= 1.2.0
```

## Installation ##
```bash
pipenv install monypy
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
    Attribute for setting up the database. Parameters:
    * `name` - the name of the database
    
    List of other optional parameters [here](https://api.mongodb.com/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient).
    
* #### `__collection__` ####
    __optional__. Attribute for setting up the collection. Parameters: 
    * `name` - the name of the collection

* #### `__abstract__` ####
    __optional__. If `True`,  then the collection will not create a connection to the database.

* #### `__loop__` ####
    __optional__. Special event loop instance to use instead of default.

* #### `__init_data__` ####
  __optional__. Sets the initializing data for all objects in the collection when the object is initialized. If the value is callable, an instance will be passed to the value and called.

* #### `manager` ####
    The class attribute for database queries.
    Example: 
    ```python
    users_count = await User.manager.count()
    assert users_count == 1
    ```
* #### `manager_class` ####
    __optional__. Set a custom manager class. [Learn more](#manager-1).

* #### `_as_dict()` ####
    Returns the object as a __dict__.
    
* #### `save()` ####
    __сoroutine__. Saves the object in the database if it does not exist, if it exists, it updates.

* #### `delete()` ####
    __сoroutine__. Removes an object from the database. If the object does not exist, then the __DocumentDoesNotExistError__ exception is raised.

* #### `refresh()` ####
    __сoroutine__. Updates an object from the database. If the object does not exist, then the __DocumentDoesNotExistError__ exception is raised.

### Manager ###
A simple wrapper over [AsyncIOMotorCollection](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection).
Example:
```python
from monypy import Doc, Manager

class UserManager(Manager):
    def get_active(self):
        return self.find({'active': True})
        
        
class User(Doc):
    manager_class = UserManager

    __database__ = {
        'name': 'test'
    }
    
    __init_data__ = {
        'active': True,
    }

await User().save()
await User(active=False).save()

assert await User.manager.count() == 2
assert await User.manager.get_active().count() == 1

assert len([u async for u in User.manager.get_active()]) == 1

```