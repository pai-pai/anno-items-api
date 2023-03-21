from flask import Flask

from app.database import mongo


def create_app(db_uri: str) -> Flask:
    app = Flask(__name__)

    app.config["MONGO_URI"] = db_uri
    mongo.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    return app
