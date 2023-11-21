#!/usr/bin/python3
"""Defines a view for the Place object"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Lists all PLaces in a City"""
    select_city = storage.get(City, city_id)
    if select_city is None:
        abort(404)
    places_list = []
    for places in storage.all(Place).values():
        if places.city_id == city_id:
            places_list.append(places.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>',
                 methods=["GET"], strict_slashes=False)
def get_place_by_id(place_id):
    """Gets a specific Place"""
    select_place = storage.get(Place, place_id)
    if select_place is None:
        abort(404)
    else:
        return jsonify(select_place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Deletes an A Place with an ID and returns code 200.
        Returns 404 code if Place not found
    """
    select_place = storage.get(Place, place_id)
    if select_place is None:
        abort(404)
    storage.delete(select_place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    select_city = storage.get(City, city_id)
    if select_city is None:
        abort(404)
    new_dict = request.get_json(silent=True)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in new_dict.keys() or new_dict["name"] is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    elif "user_id" not in new_dict.keys() or new_dict["user_id"] is None:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    select_user = storage.get(User, new_dict["user_id"])
    if select_user is None:
        abort(404)
    new_place = Place(**new_dict)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>",
                 methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates specified Place"""
    new_dict = request.get_json(silent=True)
    select_place = storage.get(Place, place_id)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if select_place is None:
        abort(404)
    ignore = ["id", "user_id", "city_id", "email", "created_at", "updated_at"]
    for key, value in new_dict.items():
        if key in ignore:
            continue
        setattr(select_place, key, value)
    storage.save()
    return make_response(jsonify(select_place.to_dict()), 200)
