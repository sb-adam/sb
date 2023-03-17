from flask import Blueprint, request, jsonify
from ..models import Comment
from ..schemas import CommentSchema
from ..utils.auth import require_auth

replies_blueprint = Blueprint("replies", __name__)
comment_schema = CommentSchema()

@replies_blueprint.route("/comments/<int:comment_id>/replies", methods=["POST"])
@require_auth
def create_reply(comment_id, authenticated_user_id):
    data = request.get_json()
    reply = Comment(user_id=authenticated_user_id, parent_id=comment_id, text=data["text"])
    reply.save()
    return comment_schema.jsonify(reply), 201

@replies_blueprint.route("/comments/<int:comment_id>/replies", methods=["GET"])
def get_replies(comment_id):
    replies = Comment.query.filter_by(parent_id=comment_id).all()
    return comment_schema.jsonify(replies, many=True), 200

