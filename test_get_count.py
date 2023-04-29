#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.city import City

# my_state = storage.get("State", "9d796a6d-14ea-4e49-845e-fd73ebf2693e")
# print(my_state.to_dict())
# print()
new_state = storage.get(State, "17d57eba-dc36-456d-8fc6-df09cf084f42")

print()
_dict = {"name": "Osun is cool"}
new_state.name = _dict["name"]
storage.save()