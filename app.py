from flask import Flask, jsonify
from flask_cors import CORS
from api.endpoints import api_blueprint
import config
from flask_sqlalchemy import SQLAlchemy
from api.database import db
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)
jwt = JWTManager(app)
# CORS(app)

app.register_blueprint(api_blueprint, url_prefix='/api/v1')

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
