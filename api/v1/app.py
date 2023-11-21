#!/usr/bin/python3
"""Creates a Flask instance"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear_down(close):
    """Method that calls storage.close"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    return jsonify({"error": "Not found"}), 404


host = getenv("HBNB_API_HOST", default="0.0.0.0")
port = getenv("HBNB_API_PORT", default="5000")

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
