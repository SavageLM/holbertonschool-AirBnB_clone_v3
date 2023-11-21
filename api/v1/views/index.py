#!/usr/bin/python3
"""Creates a route for the Status page"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def display_status():
    display = {"status": "OK"}
    return jsonify(display)
