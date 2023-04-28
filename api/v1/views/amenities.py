#!/usr/bin/python3
""" Contains routes that manages objects of class State
with HTTP methods
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET', 'POST'])
def get_amenities():
    """Returns a list of all Amenity objects or
    create a new Amenity object depending on the HTTP method
    """
    all_amenities = storage.all("Amenity").values()

    if request.method == 'GET':
        amenities_list = [obj.to_dict() for obj in all_amenities]
        return jsonify(amenities_list)

    if request.method == 'POST':
        if not request.json:
            return make_response(jsonify("Not a JSON"), 400)
        if 'name' not in request.json:
            return make_response(jsonify("Missing name"), 400)

        request_dict = request.get_json()
        new_obj = Amenity(**request_dict)
        new_obj.save()
        return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['GET', 'PUT'])
def get_update_amenity(amenity_id):
    """Return or Update an Amenity object by its id """
    amenity_obj = storage.get("Amenity", amenity_id)

    if amenity_obj:

        if request.method == 'GET':
            return jsonify(amenity_obj.to_dict())

        if request.method == 'PUT':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            request_dict = request.get_json()
            amenity_obj.name = request_dict.get("name")
            amenity_obj.save()
            return make_response(jsonify(amenity_obj.to_dict()), 200)

    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """ deletes an Amenity object by its id, otherwise if
    object is not in the storage, 404 status code is returned
    """
    obj = storage.get("Amenity", amenity_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)
    abort(404)
