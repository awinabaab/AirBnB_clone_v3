#!/usr/bin/python3
"""Handles requests for Place_Amenity objects"""

from api.v1.views import app_views
from flask import make_response, request, abort, jsonify
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=['GET'])
def get_place_amenities(place_id=None):
    """Retrieves a list of all Amenity objects of a Place object
    linked to place_id

    params:
        place_id (str): id attribute of the Place object

    Returns:
        404 error if place_id is not linked to any Place object
        200 and a list of Amenity objects of the Place object in JSON"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        amenity_list = place.amenities
    else:
        amenity_list = [amenity.to_dict() for amenity in place.amenities]

    response = make_response(jsonify(amenity_list))

    return response


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE']
                 )
def delete_place_amenity_by_id(place_id=None, amenity_id=None):
    """Deletes an Amenity object linked to amenity_id to a Place object
    linked to place_id

    params:
        place_id (str): id attribute of the Place object
        amenity_id (str): id attribute of the Amenity object

    Returns:
        404 error if place_id is not linked to any Place object
        404 error if amenity_id is not linked to any Amenity object
        404 error if the Amenity object is not linked to the Place object
        200 error and an empty dictionary"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        place_amenity = any(amenity.id == amen for amen in place.amenities)
    else:
        place_amenity = any(amenity.id == amen.id for amen in place.amenities)

    if not place_amenity:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        place.amenities.remove(amenity_id)
    else:
        amenity.delete()
    storage.save()

    response = make_response(jsonify({}))

    return response


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST']
                 )
def create_place_amenity(place_id=None, amenity_id=None):
    """Links an Amenity object to a Place object

    params:
        place_id (str): id attribute of the Place object
        amenity_id (str): id attribute of the Amenity object

    Returns:
        404 error if place_id is not linked to any Place object
        404 error if amenity_id is not linked to any Amenity object
        404 error if the Amenity object is not linked to the Place object
        200 if the Amenity object is already linked to the Place object
        201 upon sucessfully linking the Place object to the Amenity object"""

    response = ""
    place_amenity = ""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if getenv("HBNB_STORAGE_TYPE") != "db":
        place_amenity = any(amenity.id == amen for amen in place.amenities)
    else:
        place_amenity = any(amenity.id == ame.id for ame.id in place.amenities)

    if not place_amenity:
        if getenv("HBNB_TYPE_STORAGE") != "db":
            if "amenity_ids" not in place.to_dict().keys():
                setattr(place, "amenity_ids", list())
            place.amenities = amenity
        else:
            place.amenities.append(amenity)
        place.save()
        response = make_response(jsonify(amenity.to_dict()), 200)
    else:
        response = make_response(jsonify(amenity.to_dict()), 200)

    return response
