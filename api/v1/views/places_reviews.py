#!/usr/bin/python3
"""Defines a view for the Review object"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def get_review_by_place(place_id):
    """Lists all Reviews for a Place"""
    select_place = storage.get(Place, place_id)
    if select_place is None:
        abort(404)
    reviews_list = []
    for reviews in storage.all(Review).values():
        if reviews.place_id == place_id:
            reviews_list.append(reviews.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>',
                 methods=["GET"], strict_slashes=False)
def get_review_by_id(review_id):
    """Gets a specific Review"""
    select_review = storage.get(Review, review_id)
    if select_review is None:
        abort(404)
    else:
        return jsonify(select_review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Deletes an A Review with an ID and returns code 200.
        Returns 404 code if Review not found
    """
    select_review = storage.get(Review, review_id)
    if select_review is None:
        abort(404)
    storage.delete(select_review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    select_place = storage.get(Place, place_id)
    if select_place is None:
        abort(404)
    new_dict = request.get_json(silent=True)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "text" not in new_dict.keys() or new_dict["text"] is None:
        return make_response(jsonify({"error": "Missing text"}), 400)
    elif "user_id" not in new_dict.keys() or new_dict["user_id"] is None:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    select_user = storage.get(User, new_dict["user_id"])
    if select_user is None:
        abort(404)
    new_dict["place_id"] = place_id
    new_review = Review(**new_dict)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates specified Place"""
    new_dict = request.get_json(silent=True)
    select_review = storage.get(Review, review_id)
    if new_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if select_review is None:
        abort(404)
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in new_dict.items():
        if key in ignore:
            continue
        setattr(select_review, key, value)
    storage.save()
    return make_response(jsonify(select_review.to_dict()), 200)
