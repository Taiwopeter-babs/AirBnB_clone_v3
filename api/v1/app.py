#!/usr/bin/python3
"""
This module contains the flask app factory
"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
# set Cross-origin resource sharing origin header
CORS(app, origin='0.0.0.0')
app.url_map.strict_slashes = False

# Register blueprints
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db_conn(error):
    """Closes the connection after every request"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Manages the 404 response error message"""
    error_msg = {
        "error": "Not found"
    }
    return make_response(jsonify(error_msg), 404)


if __name__ == "__main__":
    HOST = os.getenv("HBNB_API_HOST")
    PORT = os.getenv("HBNB_API_PORT")

    api_host = HOST if HOST else "0.0.0.0"
    api_port = PORT if PORT else "5000"

    app.run(host=api_host, port=api_port, threaded=True)
