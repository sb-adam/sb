from flask import Blueprint, request, jsonify
from ..models import Profile
from ..schemas import ProfileSchema
from ..utils.auth import require_auth

profiles_blueprint = Blueprint("profiles", __name__)
profile_schema = ProfileSchema()

@profiles_blueprint.route("/users/<int:user_id>/profile", methods=["GET"])
def get_profile(user_id):
    profile = Profile.query.filter_by(user_id=user_id).first()
    if profile:
        return profile_schema.jsonify(profile), 200
    else:
        return jsonify({"error": "Profile not found"}), 404

@profiles_blueprint.route("/users/<int:user_id>/profile", methods=["PUT"])
@require_auth
def update_profile(user_id, authenticated_user_id):
    if user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to update this profile"}), 403

    profile_data = request.get_json()
    profile = Profile.query.filter_by(user_id=user_id).first()
    if profile:
        profile.update(**profile_data)
        return profile_schema.jsonify(profile), 200
    else:
        return jsonify({"error": "Profile not found"}), 404

@profiles_blueprint.route("/users/<int:user_id>/profile", methods=["DELETE"])
@require_auth
def delete_profile(user_id, authenticated_user_id):
    if user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to delete this profile"}), 403

    profile = Profile.query.filter_by(user_id=user_id).first()
    if profile:
        profile.delete()
        return jsonify({"message": "Profile deleted"}), 200
    else:
        return jsonify({"error": "Profile not found"}), 404
