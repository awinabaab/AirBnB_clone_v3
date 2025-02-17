#!/usr/bin/python3
"""Handles requests for User objects"""

from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users", methods=['GET'])
def get_all_users():
    """Retrieves all User objects

    params: None

    Returns:
        200 and a list of all User objects in JSON"""

    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]

    response = make_response(jsonify(user_list))

    return response


@app_views.route("/users/<user_id>", methods=['GET'])
def get_user_by_id(user_id=None):
    """Retrieves a User linked to user_id

    params:
        user_id (str): id attribute of the User object

    Returns:
        404 error if user_id is not linked to any User object
        200 and the User object in JSON if user_id is
        linked to a User object"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    response = make_response(jsonify(user.to_dict()))

    return response


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user_by_id(user_id=None):
    """Deletes a User object linked to user_id

    params:
        user_id (str): id attribute of the User object

    Returns:
        404 error if user_id is not linked to any User object
        200 and an empty dictionary upon successful deletion"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user.delete()
    storage.save()

    response = make_response(jsonify({}))

    return response


@app_views.route("/users", methods=['POST'])
def create_user():
    """Creates a new User object

    params: None

    Returns:
        400 error if the request body is not a valid JSON
        400 error if the request body does not contain the key `email`
        400 error if the request body does not contain the key `password`
        201 and the User object in JSON upon successful creation"""

    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    if "email" not in request_body.keys():
        abort(400, "Missing email")

    if "password" not in request_body.keys():
        abort(400, "Missing password")

    user = User(**request_body)
    user.save()

    response = make_response(jsonify(user.to_dict()), 201)

    return response


@app_views.route("/users/<user_id>", methods=['PUT'])
def update_user_by_id(user_id=None):
    """Updates a User object linked to user_id

    params:
        user_id (str): id attribute of the User object

    Returns:
        404 error if user_id is not linked to any User object
        400 error if the request body is not a valid JSON
        200 and the updated User object in JSON upon successful update"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    request_body.pop('id', None)
    request_body.pop('email', None)
    request_body.pop('updated_at', None)
    request_body.pop('created_at', None)

    skip_keys = ['id', 'email', 'updated_at', 'created_at']
    for k, v in request_body.items():
        if k not in skip_keys:
            setattr(user, k, v)

    user.save()

    response = make_response(jsonify(user.to_dict()))

    return response
