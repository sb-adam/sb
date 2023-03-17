from flask import Flask
from api.database import db
from api.endpoints import api_blueprint
from flask_jwt_extended import JWTManager


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    jwt = JWTManager(app)
    jwt.init_app(app)
    db.init_app(app)

    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app, jwt