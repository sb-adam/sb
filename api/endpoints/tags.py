from flask import Blueprint, request, jsonify
from ..models import UserTag
from ..schemas import UserTagSchema
from ..utils.auth import require_auth

tags_blueprint = Blueprint("tags", __name__)
user_tag_schema = UserTagSchema()

@tags_blueprint.route("/users/<int:user_id>/tags", methods=["POST"])
@require_auth
def create_tag(user_id, authenticated_user_id):
    if user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to create a tag for this user"}), 403

    data = request.get_json()
    tag = UserTag(user_id=user_id, name=data["name"])
    tag.save()
    return user_tag_schema.jsonify(tag), 201

@tags_blueprint.route("/users/<int:user_id>/tags", methods=["GET"])
@require_auth
def get_tags(user_id, authenticated_user_id):
    if user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to view this user's tags"}), 403

    tags = UserTag.query.filter_by(user_id=user_id).all()
    return user_tag_schema.jsonify(tags, many=True), 200

@tags_blueprint.route("/users/<int:user_id>/tags/<int:tag_id>", methods=["PUT"])
@require_auth
def update_tag(user_id, tag_id, authenticated_user_id):
    if user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to update this user's tag"}), 403

    tag = UserTag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found"}), 404

    data = request.get_json()
    tag.name = data["name"]
    tag.save()
    return user_tag_schema.jsonify(tag), 200

@tags_blueprint.route("/users/<int:user_id>/tags/<int:tag_id>", methods=["DELETE"])
@require_auth
def delete_tag(user_id, tag_id, authenticated_user_id):
    if user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to delete this user's tag"}), 403

    tag = UserTag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found"}), 404

    tag.delete()
    return jsonify({"message": "Tag deleted"}), 200
