#!/usr/bin/python3
"""Handles request fro City objects"""

from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def get_state_cities(state_id=None):
    """Retrieves a list of City objects of a State object

    params:
        state_id (str): id attribute of the State object

    Returns:
        404 error if state_id is not linked to any State object
        200 and a list of City objects in JSON of a State object if state_id
        is linked to a State object"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]

    response = make_response(jsonify(cities))

    return response


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_city_by_id(city_id=None):
    """Retrieves a City object linked to city_id

    params:
        city_id (str): id attribute of the City object

    Returns:
        404 error if city_id is not linked to any City object
        200 and the City object in JSON if city_id is linked to a
        City object"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    response = make_response(jsonify(city.to_dict()))

    return response


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city_by_id(city_id=None):
    """Deletes a City object linked to city_id

    params:
        city_id (str): id attribute of the City object

    Returns:
        404 error if the city_id is not linked to any City object
        200 and an empty dictionary if the City object was
        deleted successfully"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    response = make_response(jsonify({}))

    return response


@app_views.route("/states/<state_id>/cities/", methods=['POST'])
def create_city(state_id=None):
    """Creates a City object

    params:
        state_id (str): state_id attribute of the City object

    Returns:
        404 error if state_id is not linked to any State object
        400 error if the request body is not a valid JSON
        400 error if the request body does not contain the key `name`
        201 and the City object upon succesful creation"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    request_body = ""
    if request.is_json:
        request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    if "name" not in request_body.keys():
        abort(400, "Missing name")

    city = City(**request_body)
    city.state_id = state_id

    city.save()

    response = make_response(jsonify(city.to_dict()), 201)

    return response


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city_by_id(city_id=None):
    """Updates a City object linked to city_id

    params:
        city_id (str): id attibute of the City object

    Returns:
        404 error if city_id is not linked to any City object
        400 if the request body is not a valid JSON
        200 and the City object upon successful update"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    request_body = ""
    if request.is_json:
        request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    skip_keys = ['id', 'state_id', 'updated_at', 'created_at']
    for k, v in request_body.items():
        if k not in skip_keys:
            setattr(city, k, v)

    city.save()

    response = make_response(jsonify(city.to_dict()))

    return response
