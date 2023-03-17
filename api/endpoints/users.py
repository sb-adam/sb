from flask import Blueprint, request, jsonify
from api.models.users import User
from api.utils.auth import require_auth, require_role
from flask_jwt_extended import get_jwt_identity
from api.schemas.users import UserSchema

users_blueprint = Blueprint("users", __name__)
user_schema = UserSchema()


@users_blueprint.route("/users", methods=["POST"])
def create_user():
    user_data = request.get_json()
    
    # Check if user with same email exists
    existing_user = User.query.filter_by(email=user_data["email"]).first()
    if existing_user:
        return jsonify({"error": "User with this email or username already exists"}), 400
    
    # Check if user with same username exists
    existing_user = User.query.filter_by(username=user_data["username"]).first()
    if existing_user:
        return jsonify({"error": "User with this email or username already exists"}), 400
    
    # Create new user
    new_user = User(**user_data)
    new_user.save()
    
    return user_schema.dump(new_user), 201

# @users_blueprint.route("/users", methods=["GET"])
# @require_auth
# # @require_role([UserRole.MODERATOR, UserRole.ADMIN])
# def get_all_users():
#     users = User.query.all()
#     return user_schema.jsonify(users, many=True), 200


@users_blueprint.route("/users/<int:user_id>", methods=["GET"])
@require_auth
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user_schema.dump(user), 200
    else:
        return jsonify({"error": "User not found"}), 404


@users_blueprint.route("/users/<int:user_id>", methods=["PUT"])
@require_auth
def update_user(user_id):
    user_data = request.get_json()
    user = User.query.get(user_id)

    # Check if user is updating their own profile
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "You are not authorized to update this user's profile"}), 401

    if user:
        user.update(**user_data)
        return user_schema.dump(user), 200
    else:
        return jsonify({"error": "User not found"}), 404


# @users_blueprint.route("/users/<int:user_id>", methods=["DELETE"])
# @require_auth
# # @require_role([UserRole.MODERATOR, UserRole.ADMIN])
# def delete_user(user_id):
#     user = User.query.get(user_id)
#     if user:
#         user.delete()
#         return jsonify({"message": "User deleted"}), 200
#     else:
#         return jsonify({"error": "User not found"}), 404

