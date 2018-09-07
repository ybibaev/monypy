# monypy - asynchronous lightweight ODM for MongoDB based on [motor](https://github.com/mongodb/motor)

[![Build Status](https://travis-ci.org/nede1/monypy.svg?branch=master)](https://travis-ci.org/nede1/monypy)

## Dependencies ##
```
python <= 3.7
motor >= 2.0
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
    
user = User(name='John')

assert '_id' not in user
assert user.name == 'John'
assert user.sex == 'male'

assert not callable(user.instance_id)
assert user.instance_id == id(user)

asyncio.run(user.save())

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

* #### `__init_data__` ####
  __optional__. Set the initializing data for all objects in the collection when the object is initialized. If the value is callable, an instance will be passed as an argument.

* #### `save()` ####
    __сoroutine__. It saves the object in the database.

* #### `delete()` ####
    __сoroutine__. It remove an object from the database. If the object does not exist in the database, then the __DocumentDoesNotExist__ exception will be raised.

* #### `refresh()` ####
    __сoroutine__. Refresh the current object from the same object from the database. If the object does not exist in the database, then the __DocumentDoesNotExist__ exception will be raised.

### Manager ###
A simple wrapper over [AsyncIOMotorCollection](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection).

* #### `create(**kwargs)` ####
    __сoroutine__. Create an object and return it.
    
* #### `count(filter, session=None, **kwargs)` ####
    __сoroutine__. Simple alias on [count_documents](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.count_documents).

For example:
```python
from monypy import Doc, Manager

class UserManager(Manager):
    async def count_active(self):
        return await self.count_documents({'active': True})

class SecondUserManager(Manager):
    async def count_not_active(self):
        return await self.count_documents({'active': False})
        
        
class User(Doc):
    documents = UserManager()
    second_documents = SecondUserManager()

    __database__ = {
        'name': 'test'
    }
    
    __init_data__ = {
        'active': True,
    }

await User().save()
await User(active=False).save()

assert await User.documents.count() == 2
assert await User.documents.count_active() == 1
assert await User.second_documents.count_not_active() == 1

```