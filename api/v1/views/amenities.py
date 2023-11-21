#!/usr/bin/python3
"""Defines a view for the Amenity object"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET"],
                 strict_slashes=False)
def get_amenities():
    """Lists all Amenities"""
    amenities_list = []
    for amenities in storage.all(Amenity).values():
        amenities_list.append(amenities.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=["GET"], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Gets a specific Amenity"""
    select_amenity = storage.get(Amenity, amenity_id)
    if select_amenity is None:
        abort(404)
    else:
        return jsonify(select_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity with an ID and returns code 200.
        Returns 404 code if Amenity not found
    """
    select_amenity = storage.get(Amenity, amenity_id)
    if select_amenity is None:
        abort(404)
    storage.delete(select_amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates an Amenity"""
    new_dict = request.get_json(silent=True)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in new_dict.keys() or new_dict["name"] is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**new_dict)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates specified Amenity"""
    new_dict = request.get_json(silent=True)
    select_amenity = storage.get(Amenity, amenity_id)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if select_amenity is None:
        abort(404)
    ignore = ["id", "created_at", "updated_at"]
    for key, value in new_dict.items():
        if key in ignore:
            continue
        setattr(select_amenity, key, value)
    storage.save()
    return make_response(jsonify(select_amenity.to_dict()), 200)
