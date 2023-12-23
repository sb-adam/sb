from flask import Blueprint, request, jsonify
from ..models import Content
from ..schemas import ContentSchema
from ..utils.auth import require_auth
from ..database import db

content_blueprint = Blueprint("content", __name__)
content_schema = ContentSchema()

@content_blueprint.route("/content", methods=["POST"])
@require_auth
def create_content(authenticated_user_id):
    data = request.get_json()
    content = Content(user_id=authenticated_user_id, title=data["title"], description=data["description"], file_url=data["file_url"], content_type=data["content_type"])
    content.save()
    result = content_schema.dump(content)  # Use dump here
    return jsonify(result), 201  # Use Flask's jsonify to return a response


@content_blueprint.route("/content", methods=["GET"])
def get_content():
    content_list = Content.query.all()
    result = content_schema.dump(content_list, many=True)  # Use dump here with many=True for a list of objects
    return jsonify(result), 200

@content_blueprint.route("/content/<int:content_id>", methods=["PUT"])
@require_auth
def update_content(content_id, authenticated_user_id):
    content = Content.query.get(content_id)
    if not content:
        return jsonify({"error": "Content not found"}), 404

    if content.user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to update this content"}), 403

    data = request.get_json()
    content.title = data["title"]
    content.description = data["description"]
    content.file_url = data["file_url"]
    content.save()
    result = content_schema.dump(content)
    return jsonify(result), 200 # Use Flask's jsonify to return a response

@content_blueprint.route("/content/<int:content_id>", methods=["DELETE"])
@require_auth
def delete_content(content_id, authenticated_user_id):
    content = Content.query.get(content_id)
    if not content:
        return jsonify({"error": "Content not found"}), 404

    if content.user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to delete this content"}), 403

    db.session.delete(content)  # Use db.session.delete() here
    db.session.commit()  # Commit the changes to the database

    return jsonify({"message": "Content deleted"}), 200
