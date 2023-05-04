#!/usr/bin/python3
""" Contains routes that manages objects of class Place
with HTTP methods
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'])
def get_places_of_city(city_id):
    """Returns a list of all Place objects linked to a City object
    with id: city_id
    """
    city_obj = storage.get("City", city_id)

    if city_obj:
        if request.method == 'GET':
            places_of_city = [obj.to_dict() for obj in city_obj.places]
            return jsonify(places_of_city)
    abort(404)


@app_views.route("/places/<place_id>", methods=['GET', 'PUT'])
def get_update_place(place_id):
    """Return a Place object by its id """
    place_obj = storage.get("Place", place_id)

    if place_obj:

        if request.method == 'GET':
            return jsonify(place_obj.to_dict())

        if request.method == 'PUT':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)

            request_dict = request.get_json()

            if "description" in request_dict:
                place_obj.description = request_dict["description"]
            if "name" in request_dict:
                place_obj.name = request_dict["name"]
            if "number_rooms" in request_dict:
                place_obj.number_rooms = request_dict["number_rooms"]
            if "number_bathrooms" in request_dict:
                place_obj.number_bathrooms = request_dict["number_bathrooms"]
            if "max_guest" in request_dict:
                place_obj.max_guest = request_dict["max_guest"]
            if "price_by_night" in request_dict:
                place_obj.price_by_night = request_dict["price_by_night"]
            if "latitude" in request_dict:
                place_obj.latitude = request_dict["latitude"]
            if "longitude" in request_dict:
                place_obj.longitude = request_dict["longitude"]

            place_obj.save()
            return make_response(jsonify(place_obj.to_dict()), 200)

    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'])
def create_place(city_id):
    """Create a new Place object linked to a City object
    with id: city_id
    """
    city_obj = storage.get("City", city_id)

    if city_obj:
        if request.method == 'POST':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            request_dict = request.get_json()

            if 'name' not in request_dict:
                return make_response(jsonify("Missing name"), 400)
            if 'user_id' not in request_dict:
                return make_response(jsonify("Missing user_id"), 400)

            # check if user exists
            user_id = request_dict.get("user_id")
            user_obj = storage.get("User", user_id)
            if not user_obj:
                abort(404)

            request_dict.update({'city_id': city_id})
            new_obj = Place(**request_dict)
            new_obj.save()
            return make_response(jsonify(new_obj.to_dict()), 201)

    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'])
def delete_place(place_id):
    """ deletes a Place object by its id, otherwise if
    object is not in the storage, 404 statuc code is returned
    """
    obj = storage.get("Place", place_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route("/places_search", methods=['GET', 'POST'])
def places_search():
    """
    This route searches for Place objects in keys `states`, `cities`,
    and `amenities` in the JSON body request.
    If the `amenities` key list is not empty, only place objects which
    have all the amenities in the list will be returned, otherwise, every
    Place object in every city in `cities` and every Place object in each
    City object in each State object in cities will be returned
    """
    if not request.json:
        return make_response(jsonify("Not a JSON"), 400)

    request_dict = request.get_json()

    if not request_dict:
        places = [obj.to_dict() for obj in storage.all("Place").values()]
        return jsonify(places)

    states = request_dict.get("states")
    cities = request_dict.get("cities")
    amenities = request_dict.get("amenities")

    if not states and not cities and not amenities:
        places = [obj.to_dict() for obj in storage.all("Places").values()]
        return jsonify(places)

    all_list = []
    if states:
        for st_id in states:
            st_obj = storage.get("State", st_id)
            if st_obj:
                for city in st_obj.cities:
                    for place in city.places:
                        all_list.append(place)

    if cities:
        for ci_id in cities:
            city_obj = storage.get("City", ci_id)
            if city_obj:
                for place in city_obj.places:
                    all_list.append(place)

    amenity_list = []
    if amenities:
        if not all_list:
            all_list = [obj for obj in storage.all("Place").values]
        for amen_id in amenities:
            am_obj = storage.get("Amenity", am_id)
            amenity_list.append(am_obj)

        """This will check each place_obj.amenities list and return either
        True or False if all the objects in amenities are in
        place_obj.amenities
        """
        all_list = [obj for obj in all_list
                    if all(am_obj in obj.amenities for am_obj in amenity_list)]

    return_list = [obj.to_dict() for obj in all_list]

    return jsonify(return_list)
