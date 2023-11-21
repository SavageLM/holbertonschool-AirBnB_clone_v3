#!/usr/bin/python3
"""Defines a view for the City object"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """Lists all Cities for a given State"""
    select_state = storage.get(State, state_id)
    if select_state is None:
        abort(404)
    cities_list = []
    for cities in storage.all(City).values():
        cities_list.append(cities.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def get_cities_by_id(city_id):
    """Gets a specific City"""
    select_city = storage.get(City, city_id)
    if select_city is None:
        abort(404)
    else:
        return jsonify(select_city.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City with an ID and returns code 200.
        Returns 404 code if State not found
    """
    select_city = storage.get(City, id)
    if select_city is None:
        abort(404)
    storage.delete(select_city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    new_dict = request.get_json(silent=True)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in new_dict.keys() or new_dict["name"] is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    select_state = storage.get(State, state_id)
    if select_state is None:
        abort(404)
    new_dict["state_id"] = state_id
    new_city = City(**new_dict)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates specified City"""
    new_dict = request.get_json(silent=True)
    select_city = storage.get(City, city_id)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if select_city is None:
        abort(404)
    ignore = ["id", "state_id", "created_at", "updated_at"]
    for key, value in new_dict.items():
        if key in ignore:
            continue
        setattr(select_city, key, value)
    storage.save()
    return make_response(jsonify(select_city.to_dict()), 200)
