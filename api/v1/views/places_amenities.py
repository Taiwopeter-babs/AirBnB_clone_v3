#!/usr/bin/python3
""" Contains routes that manages objects of class State
with HTTP methods
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, storage_t
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=['GET'])
def get_amenities_of_place(place_id):
    """Returns a list of all Amenity objects linked to a Place object
    with id: place_id
    """
    place_obj = storage.get("Place", place_id)

    if place_obj:
        if request.method == 'GET':
            if storage_t == "db":
                place_amenities = [obj.to_dict() for obj in
                                   place_obj.amenities]
                return jsonify(place_amenities)
            else:
                amenity_ids = [am_id for am_id in place_obj.amenity_ids]
                return amenity_ids
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['POST'])
def link_amenity_with_place(place_id, amenity_id):
    """Link an Amenity object with a Place object """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if place is None or amenity is None:
        abort(404)

    if storage_t == "db":
        if amenity in place.amenities:
            return (jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
        place.save()
        return make_response(jsonify(amenity.to_dict()), 201)

    else:
        if amenity_id in place.amenity_ids:
            return amenity.to_dict()
        place.amenity_ids.append(amenity_id)
        place.save()
        return amenity.to_dict()


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'])
def delete_amenity_by_place(place_id, amenity_id):
    """ deletes an Amenity object in a Place object, otherwise if
    any of the object is not in the storage or the Amenity,
    object is not linked to the Place object, a 404 error is raised
    """
    place_obj = storage.get("Place", place_id)
    amenity_obj = storage.get("Amenity", amenity_id)

    if place_obj is None or amenity_obj is None:
        abort(404)

    if storage_t == "db":
        if amenity_obj in place_obj.amenities:
            place_obj.amenities.remove(amenity)
            place_obj.save()
            return (jsonify({}), 200)
        else:
            abort(404)
    else:
        if amenity_id in place_obj.amenity_ids:
            place_obj.amenity_ids.remove(amenity_id)
            return {}
        else:
            return None
