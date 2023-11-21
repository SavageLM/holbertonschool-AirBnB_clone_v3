#!/usr/bin/python3
"""Defines a view for the States object"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def get_states():
    """Lists all States in storage"""
    states_list = []
    for states in storage.all(State).values():
        states_list.append(states.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<id>', methods=["GET"], strict_slashes=False)
def get_states_by_id(id):
    """Gets a specific state"""
    select_state = storage.get(State, id)
    if select_state is None:
        abort(404)
    else:
        return jsonify(select_state.to_dict())


@app_views.route('/states/<id>', methods=["DELETE"], strict_slashes=False)
def delete_state(id):
    """Deletes a State with an ID and returns code 200.
        Returns 404 code if State not found
    """
    select_state = storage.get(State, id)
    if select_state is None:
        abort(404)
    storage.delete(select_state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def create_state(id):
    """Creates a State"""
    new_dict = request.get_json()
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in new_dict.keys() or new_dict["name"] is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**new_dict)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("states/<id>", methods=["PUT"], strict_slashes=False)
def update_state(id):
    """Updates specified State"""
    new_dict = request.get_json()
    select_state = storage.get(State, id)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if select_state is None:
        abort(404)
    ignore = ["id", "created_at", "updated_at"]
    for key, value in new_dict.items():
        if key in ignore:
            continue
        setattr(select_state, key, value)
    storage.save()
    return make_response(jsonify(select_state.to_dict()), 200)
