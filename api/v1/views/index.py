#!/usr/bin/python3
"""Handles requests to the root of the api"""

from api.v1.views import app_views
from flask import make_response, jsonify
from models import storage


@app_views.route("/status", )
def status():
    """Returns the status of the API"""
    body = {"status": "OK"}
    response = make_response(jsonify(body))
    return response
