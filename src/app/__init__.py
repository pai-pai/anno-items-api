import os

from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    with app.app_context():
        from . import apis
    return app
