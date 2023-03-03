from flask import Flask
from flask_cors import CORS

from app.database import mongo


def create_app(db_uri: str) -> Flask:
    app = Flask(__name__)

    app.config["MONGO_URI"] = db_uri
    mongo.init_app(app)

    from . import api
    app.register_blueprint(api.bp)
    #with app.app_context():
    #    from . import api
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app
