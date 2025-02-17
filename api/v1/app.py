#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found_error(error):
    """Returns a JSON-formatted 404 status code response"""
    body = {"error": "Not found"}
    response = make_response(jsonify(body), 404)

    return response


@app.teardown_appcontext
def close(exception=None):
    """Closes the storage session after each request"""
    storage.close()


if __name__ == "__main__":
    api_host = getenv("HBNB_API_HOST", default="0.0.0.0")
    api_port = getenv("HBNB_API_PORT", default=5000)
    app.run(host=api_host, port=api_port, threaded=True)
