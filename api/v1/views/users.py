#!/usr/bin/python3
"""Defines a view for the User object"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=["GET"],
                 strict_slashes=False)
def get_users():
    """Lists all Users"""
    users_list = []
    for users in storage.all(User).values():
        users_list.append(users.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>',
                 methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """Gets a specific User"""
    select_user = storage.get(User, user_id)
    if select_user is None:
        abort(404)
    else:
        return jsonify(select_user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes an A User with an ID and returns code 200.
        Returns 404 code if User not found
    """
    select_user = storage.get(User, user_id)
    if select_user is None:
        abort(404)
    storage.delete(select_user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """Creates an user"""
    new_dict = request.get_json(silent=True)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "email" not in new_dict.keys() or new_dict["email"] is None:
        return make_response(jsonify({"error": "Missing email"}), 400)
    elif "password" not in new_dict.keys() or new_dict["password"] is None:
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**new_dict)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>",
                 methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates specified Amenity"""
    new_dict = request.get_json(silent=True)
    select_user = storage.get(User, user_id)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if select_user is None:
        abort(404)
    ignore = ["id", "email", "created_at", "updated_at"]
    for key, value in new_dict.items():
        if key in ignore:
            continue
        setattr(select_user, key, value)
    storage.save()
    return make_response(jsonify(select_user.to_dict()), 200)
