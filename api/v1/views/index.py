#!/usr/bin/python3
"""Creates a route for the Status page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def display_status():
    display = {"status": "OK"}
    return jsonify(display)


@app_views.route('/stats', methods=['GET'])
def display_stats():
    display = {}
    classes = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
    }
    for key, value in classes.items():
        display[value] = storage.count(key)
    return jsonify(display)
