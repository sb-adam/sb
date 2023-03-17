from flask import Blueprint, request, jsonify
from ..models import Comment
from ..schemas import CommentSchema
from ..utils.auth import require_auth

comment_blueprint = Blueprint("comment", __name__)
comment_schema = CommentSchema()

@comment_blueprint.route("/content/<int:content_id>/comments", methods=["POST"])
@require_auth
def create_comment(content_id, authenticated_user_id):
    data = request.get_json()
    comment = Comment(user_id=authenticated_user_id, content_id=content_id, text=data["text"])
    comment.save()
    return comment_schema.jsonify(comment), 201

@comment_blueprint.route("/content/<int:content_id>/comments", methods=["GET"])
def get_comments(content_id):
    comments = Comment.query.filter_by(content_id=content_id).all()
    return comment_schema.jsonify(comments, many=True), 200

@comment_blueprint.route("/comments/<int:comment_id>", methods=["PUT"])
@require_auth
def update_comment(comment_id, authenticated_user_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if comment.user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to update this comment"}), 403

    data = request.get_json()
    comment.text = data["text"]
    comment.save()
    return comment_schema.jsonify(comment), 200

@comment_blueprint.route("/comments/<int:comment_id>", methods=["DELETE"])
@require_auth
def delete_comment(comment_id, authenticated_user_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if comment.user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to delete this comment"}), 403

    comment.delete()
    return jsonify({"message": "Comment deleted"}), 200
