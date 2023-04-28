#!/usr/bin/python3
""" Contains a route that returns the status """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def response_status():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def get_stats_of_tables():
    """Returns the object count of each table in the database"""
    results_dict = {}

    obj_list = ["Amenity", "City", "Place", "Review", "State", "User"]
    keys_list = ["amenities", "cities", "places", "reviews", "states", "users"]
    results = [storage.count(obj) for obj in obj_list]

    results_dict = {}
    for idx, key in enumerate(keys_list):
        results_dict[keys_list[idx]] = results[idx]
    return jsonify(results_dict)
