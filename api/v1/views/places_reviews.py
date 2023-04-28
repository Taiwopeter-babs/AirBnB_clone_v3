#!/usr/bin/python3
""" Contains routes that manages objects of class State
with HTTP methods
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'])
def get_reviews_of_place(place_id):
    """Returns a list of all Review objects linked to a Place object
    with id: place_id
    """
    place_obj = storage.get("Place", place_id)
    all_reviews = storage.all("Review").values()

    if place_obj:
        if request.method == 'GET':
            reviews_of_place = [obj.to_dict() for obj in all_reviews
                                if obj.place_id == place_id]
            return jsonify(reviews_of_place)

        if request.method == 'POST':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)

            request_dict = request.get_json()

            if 'text' not in request_dict:
                return make_response(jsonify("Missing text"), 400)
            if 'user_id' not in request_dict:
                return make_response(jsonify("Missing user_id"), 400)

            # check if user exists
            user_id = request_dict.get("user_id")
            user_obj = storage.get("User", user_id)
            if not user_obj:
                abort(404)

            request_dict.update({"place_id": place_id})
            new_obj = Review(**request_dict)
            new_obj.save()
            return make_response(jsonify(new_obj.to_dict()), 201)

    abort(404)


@app_views.route("/reviews/<review_id>", methods=['GET', 'PUT'])
def get_update_review(review_id):
    """Return a Review object by its id """
    review_obj = storage.get("Review", review_id)

    if review_obj:

        if request.method == 'GET':
            return jsonify(review_obj.to_dict())

        if request.method == 'PUT':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            request_dict = request.get_json()
            review_obj.text = request_dict.get("text")
            review_obj.save()
            return make_response(jsonify(review_obj.to_dict()), 200)

    abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_review(review_id):
    """ deletes a Review object by its id, otherwise if
    object is not in the storage, 404 error is raised
    """
    obj = storage.get("Review", review_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)
    abort(404)
