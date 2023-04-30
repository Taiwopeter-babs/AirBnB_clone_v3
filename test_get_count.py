#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.user import User

# data = {"first_name":"Kenny", "last_name":"Babs", "email": "kenny@test.com", "password": "mypassword2"}
# my_user = User(**data)
# my_user.save()
my_user = storage.get("User", "d2a916b3-a2f5-4e83-926f-0c23f888b7a1")
print(my_user.to_dict())
print(my_user.password)
