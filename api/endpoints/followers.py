from flask import Blueprint, request, jsonify
from ..models import User, UserFollower
from ..schemas import UserFollowerSchema
from ..utils.auth import require_auth

followers_blueprint = Blueprint("followers", __name__)
user_follower_schema = UserFollowerSchema()

@followers_blueprint.route("/users/<int:user_id>/followers", methods=["GET"])
@require_auth
def get_followers(user_id, authenticated_user_id):
    if user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to view this user's followers"}), 403

    followers = UserFollower.query.filter_by(user_id=user_id).all()
    return user_follower_schema.jsonify(followers, many=True), 200

@followers_blueprint.route("/users/<int:user_id>/followers", methods=["PUT"])
@require_auth
def update_followers(user_id, authenticated_user_id):
    if user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to update this user's followers"}), 403

    data = request.get_json()
    follower_id = data["follower_id"]
    action = data["action"]

    if action == "add":
        follower_relation = UserFollower(user_id=user_id, follower_id=follower_id)
        follower_relation.save()
        return jsonify({"message": "Follower added"}), 200
    elif action == "remove":
        follower_relation = UserFollower.query.filter_by(user_id=user_id, follower_id=follower_id).first()
        if follower_relation:
            follower_relation.delete()
            return jsonify({"message": "Follower removed"}), 200
        else:
            return jsonify({"error": "Follower relation not found"}), 404
    else:
        return jsonify({"error": "Invalid action"}), 400
