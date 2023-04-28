#!/usr/bin/python3
""" Contains routes that manages objects of class State
with HTTP methods
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET', 'POST'])
def get_users():
    """Returns a list of all User objects or
    create a new User object depending on the HTTP method
    """
    all_users = storage.all("User").values()

    if request.method == 'GET':
        users_list = [obj.to_dict() for obj in all_users]
        return jsonify(users_list)

    if request.method == 'POST':
        if not request.json:
            return make_response(jsonify("Not a JSON"), 400)

        request_dict = request.get_json()
        if 'email' not in request_dict:
            return make_response(jsonify("Missing email"), 400)
        if 'password' not in request_dict:
            return make_response(jsonify("Missing password"), 400)

        new_obj = User(**request_dict)
        new_obj.save()
        return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['GET', 'PUT'])
def get_update_user(user_id):
    """Return or Update a User object by its id """
    user_obj = storage.get("User", user_id)

    if user_obj:

        if request.method == 'GET':
            return jsonify(user_obj.to_dict())

        if request.method == 'PUT':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            request_dict = request.get_json()

            if request_dict.get("password"):
                user_obj.password = request_dict.get("password")
            if request_dict.get("first_name"):
                user_obj.first_name = request_dict.get("first_name")
            if request_dict.get("last_name"):
                user_obj.last_name = request_dict.get("last_name")

            user_obj.save()
            return make_response(jsonify(user_obj.to_dict()), 200)

    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    """ deletes a User object by its id, otherwise if
    object is not in the storage, 404 status code is returned
    """
    obj = storage.get("User", user_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)
    abort(404)
