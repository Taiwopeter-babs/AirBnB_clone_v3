#!/usr/bin/python3
""" Contains routes that manages objects of class State
with HTTP methods
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET', 'POST'])
def get_create_state():
    """Returns a list of all State objects in their dictionary
    representation
    """
    if request.method == 'GET':
        all_states = storage.all("State").values()
        states_list = [obj.to_dict() for obj in all_states]
        return jsonify(states_list)

    elif request.method == 'POST':
        if not request.json:
            return make_response(jsonify("Not a JSON"), 400)
        if 'name' not in request.json:
            return make_response(jsonify("Missing name"), 400)

        request_dict = request.get_json()
        state_name = request_dict.get("name")
        new_obj = State(name=state_name)
        new_obj.save()
        return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['GET', 'PUT'])
def get_update_state(state_id):
    """Return a State object by its id """
    state_obj = storage.get("State", state_id)

    if state_obj:

        if request.method == 'GET':
            return jsonify(state_obj.to_dict())

        if request.method == 'PUT':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            request_dict = request.get_json()
            state_obj.name = request_dict.get("name")
            state_obj.save()
            return make_response(jsonify(state_obj.to_dict()), 200)

    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """ deletes a State object by its id, otherwise if
    object is not in the storage, 404 statuc code is returned
    """
    obj = storage.get("State", state_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)
    abort(404)
