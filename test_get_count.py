#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.user import User

# data = {"first_name":"Kenny", "last_name":"Babs", "email": "kenny@test.com", "password": "yourpassword2"}
# my_user = User(**data)
# my_user.save()
my_user = storage.get("User", "017cedf7-39b7-4a15-9331-1d53843a4844")
print(my_user.to_dict())
print(type(my_user))
