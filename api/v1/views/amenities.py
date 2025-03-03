#!/usr/bin/python3
"""Handles requests for Amenity objects"""

from api.v1.views import app_views
from flask import make_response, request, jsonify, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'])
def get_all_amenities():
    """Retrieves a list of all Amenity objects

    params: None

    Returns:
        200 and a list of all Amenity objects in JSON"""

    amenities = storage.all(Amenity)
    amenity_list = [amenity.to_dict() for amenity in amenities.values()]

    response = make_response(jsonify(amenity_list))

    return response


@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def get_amenity_by_id(amenity_id=None):
    """Retrieves an Amenity object by id

    params:
        amenity_id (str): id attribute of the Amenity object

    Returns:
        404 error if amenity_id is not linked to any Amenity object
        200 and the Amenity object in JSON if amenity_id is
        linked to an Amenity object"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    response = make_response(jsonify(amenity.to_dict()))

    return response


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity_by_id(amenity_id=None):
    """Deletes an Amenity object by id

    params:
        amenity_id (str): id attribute of the Amenity object

    Returns:
        404 error if amenity_id is not linked to any Amenity object
        200 and an empty dictionary upon successful deletion"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()

    response = make_response(jsonify({}))

    return response


@app_views.route("/amenities", methods=['POST'])
def create_amenity():
    """Creates a new Amenity object

    params: None

    Returns:
        400 error if the request body is not a valid JSON
        400 error if the request body does not contain the key `name`
        201 and the Amenity object in JSON upon successful creation"""

    request_body = ""
    if request.is_json:
        request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    if "name" not in request_body.keys():
        abort(400, "Missing name")

    amenity = Amenity(**request_body)
    amenity.save()

    response = make_response(jsonify(amenity.to_dict()), 201)

    return response


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update_amenity(amenity_id=None):
    """Updates an existing Amenity object

    params:
        amenity_id (str): id attribute of the Amenity object

    Returns:
        404 error if amenity_id is not linked to any Amenity object
        400 error if the request body is not a valid JSON
        200 and the updated Amenity object in JSON upon successful update"""

    request_body = ""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.is_json:
        request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    skip_keys = ['id', 'created_at', 'updated_at']
    for k, v in request_body.items():
        if k not in skip_keys:
            setattr(amenity, k, v)

    amenity.save()

    response = make_response(jsonify(amenity.to_dict()))

    return response
