from flask import Blueprint, request, jsonify
from ..models import User, UserFollower
from ..schemas import UserFollowerSchema
from ..utils.auth import require_auth

following_blueprint = Blueprint("following", __name__)
user_follower_schema = UserFollowerSchema()

@following_blueprint.route("/users/<int:user_id>/following", methods=["GET"])
@require_auth
def get_following(user_id, authenticated_user_id):
    if user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to view this user's following list"}), 403

    following = UserFollower.query.filter_by(follower_id=user_id).all()
    return user_follower_schema.jsonify(following, many=True), 200

@following_blueprint.route("/users/<int:user_id>/following", methods=["PUT"])
@require_auth
def update_following(user_id, authenticated_user_id):
    if user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to update this user's following list"}), 403

    data = request.get_json()
    following_id = data["following_id"]
    action = data["action"]

    if action == "add":
        following_relation = UserFollower(user_id=following_id, follower_id=user_id)
        following_relation.save()
        return jsonify({"message": "User added to following list"}), 200
    elif action == "remove":
        following_relation = UserFollower.query.filter_by(user_id=following_id, follower_id=user_id).first()
        if following_relation:
            following_relation.delete()
            return jsonify({"message": "User removed from following list"}), 200
        else:
            return jsonify({"error": "Following relation not found"}), 404
    else:
        return jsonify({"error": "Invalid action"}), 400
