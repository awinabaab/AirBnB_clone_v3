#!/usr/bin/python3
"""Handles requests for state objects"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'])
def get_all_states():
    """Retrieves a list of all State objects

    params: None

    Returns:
        200 and a list of all State objects in JSON"""

    states = storage.all(State)
    state_list = [state.to_dict() for state in states.values()]

    response = make_response(jsonify(state_list))

    return response


@app_views.route("/states/<state_id>", methods=['GET'])
def get_state_by_id(state_id=None):
    """Retrieves a State object linked to state_id

    params:
        state_id (str): id attribute of the State object

    Returns:
        404 error if state_id is not linked to any State object"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    response = make_response(jsonify(state.to_dict()))

    return response


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state_by_id(state_id=None):
    """Deletes a State object linked state_id

    params:
        state_id (str): id attribute of the State object

    Returns:
        404 error if state_id is not linked to any State object
        200 and an empty dictionary upon successful deletion"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    response = make_response(jsonify({}))

    return response


@app_views.route("/states", methods=['POST'])
def create_state():
    """Creates a State object

    params: None

    Returns:
        400 error if the request body is not a valid JSON
        400 error if the request body doesn't contain the key `name`
        201 and the State object upon successful creation"""
    request_body = ""
    if request.is_json:
        request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    if "name" not in request_body.keys():
        abort(400, "Missing name")

    state = State(**request_body)
    state.save()

    response = make_response(jsonify(state.to_dict()), 201)

    return response


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state_by_id(state_id=None):
    """Updates an existing State object

    params:
        state_id (str): id attribute of the State object

    Returns:
        404 error if state_id is not linked to any State"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    request_body = ""
    if request.is_json:
        request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    skip_keys = ['id', 'created_at', 'updated_at']
    for k, v in request_body.items():
        if k not in skip_keys:
            setattr(state, k, v)

    state.save()

    response = make_response(jsonify(state.to_dict()))

    return response
