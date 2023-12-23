from flask import Blueprint, request, jsonify
from ..models import Comment
from ..schemas import CommentSchema
from ..utils.auth import require_auth
from ..database import db  # Ensure you have this import

comment_blueprint = Blueprint("comment", __name__)
comment_schema = CommentSchema()

@comment_blueprint.route("/content/<int:content_id>/comments", methods=["POST"])
@require_auth
def create_comment(content_id, authenticated_user_id):
    data = request.get_json()
    comment = Comment(user_id=authenticated_user_id, content_id=content_id, text=data["text"])
    db.session.add(comment)  # Save the comment
    db.session.commit()
    return jsonify(comment_schema.dump(comment)), 201  # Serialize and return the comment

@comment_blueprint.route("/content/<int:content_id>/comments", methods=["GET"])
def get_comments(content_id):
    comments = Comment.query.filter_by(content_id=content_id).all()
    return jsonify(comment_schema.dump(comments, many=True)), 200  # Serialize and return the comments

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
    db.session.commit()  # Save the changes
    return jsonify(comment_schema.dump(comment)), 200  # Serialize and return the updated comment

@comment_blueprint.route("/comments/<int:comment_id>", methods=["DELETE"])
@require_auth
def delete_comment(comment_id, authenticated_user_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if comment.user_id != authenticated_user_id:
        return jsonify({"error": "You are not authorized to delete this comment"}), 403

    db.session.delete(comment)  # Mark the comment for deletion
    db.session.commit()  # Commit the deletion
    return jsonify({"message": "Comment deleted"}), 200
