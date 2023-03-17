from flask import Flask
from api.database import db
from api.endpoints import api_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)

    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app