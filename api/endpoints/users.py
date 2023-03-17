from flask import Blueprint, request, jsonify
from api.models.users import User
from api.utils.auth import require_auth, require_admin
from api.schemas.users import UserSchema

users_blueprint = Blueprint("users", __name__)
user_schema = UserSchema()


@users_blueprint.route("/users", methods=["POST"])
def create_user():
    user_data = request.get_json()
    new_user = User(**user_data)
    new_user.save()
    return user_schema.jsonify(new_user), 201


@users_blueprint.route("/users", methods=["GET"])
@require_auth
@require_admin
def get_all_users():
    users = User.query.all()
    return user_schema.jsonify(users, many=True), 200


@users_blueprint.route("/users/<int:user_id>", methods=["GET"])
@require_auth
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user_schema.jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404


@users_blueprint.route("/users/<int:user_id>", methods=["PUT"])
@require_auth
def update_user(user_id):
    user_data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.update(**user_data)
        return user_schema.jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404


@users_blueprint.route("/users/<int:user_id>", methods=["DELETE"])
@require_auth
@require_admin
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.delete()
        return jsonify({"message": "User deleted"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

