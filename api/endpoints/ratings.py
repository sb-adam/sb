from flask import Blueprint, request, jsonify
from ..models import Rating
from ..schemas import RatingSchema
from ..utils.auth import require_auth

ratings_blueprint = Blueprint("ratings", __name__)
rating_schema = RatingSchema()

@ratings_blueprint.route("/ratings", methods=["POST"])
@require_auth
def create_rating(authenticated_user_id):
    data = request.get_json()
    rating = Rating(user_id=authenticated_user_id, content_id=data["content_id"], value=data["value"], review=data.get("review"))
    rating.save()
    return rating_schema.jsonify(rating), 201

@ratings_blueprint.route("/ratings", methods=["GET"])
@require_auth
def get_ratings(authenticated_user_id):
    ratings = Rating.query.all()
    return rating_schema.jsonify(ratings, many=True), 200

@ratings_blueprint.route("/ratings/<int:rating_id>", methods=["PUT", "DELETE"])
@require_auth
def update_delete_rating(rating_id, authenticated_user_id):
    rating = Rating.query.get_or_404(rating_id)

    if rating.user_id != authenticated_user_id:
        return jsonify({"message": "You can only update or delete your own ratings"}), 403

    if request.method == "PUT":
        data = request.get_json()
        rating.update(data)
        return rating_schema.jsonify(rating), 200

    elif request.method == "DELETE":
        rating.delete()
        return jsonify({"message": "Rating deleted successfully"}), 204
