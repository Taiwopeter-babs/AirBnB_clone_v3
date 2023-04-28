#!/usr/bin/python3
""" Contains routes that manages objects of class State
with HTTP methods
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def get_cities_of_state(state_id):
    """Returns a list of all City objects linked to a State object
    with id: state_id
    """
    state_obj = storage.get("State", state_id)

    if state_obj:
        if request.method == 'GET':
            cities_of_state = [obj.to_dict() for obj in state_obj.cities]
            return jsonify(cities_of_state)
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def create_city(state_id):
    """Create a new City object linked to a State object
    with id: state_id
    """
    state_obj = storage.get("State", state_id)

    if state_obj:
        if request.method == 'POST':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            if 'name' not in request.json:
                return make_response(jsonify("Missing name"), 400)

            request_dict = request.get_json()
            request_dict.update({'state_id': state_id})
            new_obj = City(**request_dict)
            new_obj.save()
            return make_response(jsonify(new_obj.to_dict()), 201)
    abort(404)


@app_views.route("/cities/<city_id>", methods=['GET', 'PUT'])
def get_update_city(city_id):
    """Return a State object by its id """
    city_obj = storage.get("City", city_id)

    if city_obj:

        if request.method == 'GET':
            return jsonify(city_obj.to_dict())

        if request.method == 'PUT':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            request_dict = request.get_json()
            city_obj.name = request_dict.get("name")
            city_obj.save()
            return make_response(jsonify(city_obj.to_dict()), 200)

    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    """ deletes a State object by its id, otherwise if
    object is not in the storage, 404 statuc code is returned
    """
    obj = storage.get("City", city_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)
    abort(404)
