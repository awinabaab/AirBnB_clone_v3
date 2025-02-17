#!/usr/bin/python3
"""Handles requests for Place objects"""

from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=['GET'])
def get_city_places(city_id=None):
    """Retrieves all Place objects of a City object

    params:
        city_id (str): id attribute of the City object

    Returns:
        404 error if city_id is not linked to a City object
        200 and a list of all City objects of the Place object in JSON"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]

    response = make_response(jsonify(places))

    return response


@app_views.route("/places/<place_id>", methods=['GET'])
def get_place_by_id(place_id=None):
    """Retrieves a Place object linked to place_id

    params:
        place_id (str): id attribute of the Place object

    Returns:
        404 error if place_id is not linked to a Place object
        200 and the Place object in JSON if place_id is linked
        to a Place object"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    response = make_response(jsonify(place.to_dict()))

    return response


@app_views.route("/places/<place_id>", methods=['DELETE'])
def delete_place_by_id(place_id):
    """Deletes a Place object linked to place_id

    params:
        place_id (str): id attribute of the Place object

    Returns:
        404 if place_id is not linked to a Place object
        200 and an empty dictionary upon successful deletion"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place.delete()
    storage.save()

    response = make_response(jsonify({}))

    return response


@app_views.route("/cities/<city_id>/places", methods=['POST'])
def create_place(city_id=None):
    """Creates a new Place object

    params:
        city_id (str): id attribute of the City object

    Returns:
        404 error if city_id is not linked to any City object
        400 error if the request body is not a valid JSON
        400 error if the request body does not cotain the key `user_id`
        404 error if user_id is not linked to a User object
        400 error if the request body does not cotain the key `name`
        201 and the Place object in JSON upon successful creation"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    if "user_id" not in request_body.keys():
        abort(400, "Missing user_id")

    user_id = request_body.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if "name" not in request_body.keys():
        abort(400, "Missing name")

    place = Place(**request_body)
    place.city_id = city_id
    place.save()

    response = make_response(jsonify(place.to_dict()), 201)

    return response


@app_views.route("/places/<place_id>", methods=['PUT'])
def update_place_by_id(place_id=None):
    """Updates a Place object linked to place_id

    params:
        place_id (str): id attribute of the Place object

    Returns:
        404 error if place_id is not linked to any Place object
        400 if the request body is not a valid JSON
        200 and the updated Place object in JSON upon successful update"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    skip_keys = ['id', 'city_id', 'user_id', 'created_at', 'updated_at']
    for k, v in request_body.items():
        if k not in skip_keys:
            setattr(place, k, v)

    place.save()

    response = make_response(jsonify(place.to_dict()))

    return response
