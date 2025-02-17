#!/usr/bin/python3
"""Handles requests for Review objects"""

from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_place_reviews(place_id=None):
    """Retrieves the Reviews of a Place linked to place_id

    params:
        place_id (str): id attribute of the Place object

    Returns:
        404 error if place_id is not linked to any Place object
        200 and a list of Review object linked to the Place object"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place_reviews = [review.to_dict() for review in place.reviews]

    response = make_response(jsonify(place_reviews))

    return response


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review_by_id(review_id=None):
    """Retrives a Review object linked to review_id

    params:
        review_id (str): id attribute of the Review object

    Returns:
        404 error if review_id is not linked to any Review object
        200 and the Review object in JSON if review is
        linked to a Review object"""

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    response = make_response(jsonify(review.to_dict()))

    return response


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_review_by_id(review_id=None):
    """Deletes a Review linked to review_id

    params:
        review_id (str): id attribute of the review object

    Returns:
        404 if review_id is not linked to any Review object
        200 and an empty dictionary upon successful deletion"""

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    review.delete()
    storage.save()

    response = make_response(jsonify({}))

    return response


@app_views.route("/places/<place_id>/reviews", methods=['POST'])
def create_review(place_id=None):
    """Creates a Review object linked to a Place object

    params:
        place_id (str): id attribute of the Place object

    Returns:
        404 error if place_id is not linked to any Place object
        400 error if the request body is not a valid JSON
        400 error if the request body does not contain the key `user_id`
        404 error if `user_id` is not linked to any User object
        400 error if the request body does not contain the key `text`
        201 and the Review object in JSON upon successful creation"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    if "user_id" not in request_body.keys():
        abort(400, "Missing user_id")

    user_id = request_body.get('user_id')
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if "text" not in request_body.keys():
        abort(400, "Missing text")

    review = Review(**request_body)
    review.place_id = place_id
    review.save()

    response = make_response(jsonify(review.to_dict()), 201)

    return response


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def update_a_review_by_id(review_id=None):
    """Updates a Review linked to review_id

    params:
        review_id (str): id attribute of the Review object

    Returns:
        404 if review_id is not linked to any Review object
        400 if the request body is not a valid JSON
        200 and the updated Review object in JSON upon successful update"""

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    request_body.pop('id', None)
    request_body.pop('user_id', None)
    request_body.pop('place_id', None)
    request_body.pop('created_at', None)
    request_body.pop('updated_at', None)

    skip_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for k, v in request_body.items():
        if k not in skip_keys:
            setattr(review, k, v)

    review.save()

    response = make_response(jsonify(review.to_dict()))

    return response
