#!/usr/bin/python3
"""Handles requests to the root of the api"""

from api.v1.views import app_views
from flask import make_response, jsonify
from models import storage


@app_views.route("/status")
def status():
    """Returns the status of the API"""
    body = {"status": "OK"}
    response = make_response(jsonify(body))
    return response


@app_views.route("/stats")
def stats():
    """Retrieves the number of each object by type"""
    obj_count = {}
    objs = storage.all()
    types = {
             "Amenity": "amenities",
             "City": "cities",
             "Place": "places",
             "Review": "reviews",
             "State": "states",
             "User": "users"
             }

    for v in objs.values():
        obj_type = v.__class__.__name__
        if obj_type in types.keys():
            obj_count[types.get(obj_type)] = storage.count(v.__class__)

    response = make_response(jsonify(obj_count))

    return response
