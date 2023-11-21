#!/usr/bin/python3
"""Creates a Flask instance"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app.views)


@app.terardown_appcontext
def tear_down():
    """Method that calls storage.close"""
    storage.close()


@app.errorhandler(404)
def error_404():
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default="5000")
    app.run(host=host, port=port, threaded=True)
