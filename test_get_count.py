#!/usr/bin/python3
""" Test .get() and .count() methods
"""
import hashlib
from models import storage
from models.user import User
from models.place import Place
from models.amenity import Amenity

my_user = storage.get("User", "aad1882a-0ec3-48b1-91f9-a803ca53deb6")
print(my_user.to_dict())
print(my_user.password)

place = storage.get("Place", "02d9a2b5-7dca-423f-8406-707bc76abf7e")
amenity = storage.get("Amenity", "017ec502-e84a-4a0f-92d6-d97e27bb6bdf")
amenity = Amenity(name="Taiwo's Lair")
# amenity.save()

