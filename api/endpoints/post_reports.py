from flask import Blueprint, request, jsonify
from ..models import PostReport, UserRole
from ..schemas import PostReportSchema
from ..utils.auth import require_auth, require_role

post_reports_blueprint = Blueprint("post_reports", __name__)
post_report_schema = PostReportSchema()

@post_reports_blueprint.route("/reports", methods=["POST"])
@require_auth
def create_post_report(authenticated_user_id):
    data = request.get_json()
    post_report = PostReport(user_id=authenticated_user_id, content_id=data["content_id"], reason=data["reason"])
    post_report.save()
    return post_report_schema.jsonify(post_report), 201

@post_reports_blueprint.route("/reports", methods=["GET"])
@require_auth
@require_role([UserRole.MODERATOR, UserRole.ADMIN])
def get_post_reports(authenticated_user_id):
    post_reports = PostReport.query.all()
    return post_report_schema.jsonify(post_reports, many=True), 200

@post_reports_blueprint.route("/reports/<int:report_id>", methods=["PUT", "DELETE"])
@require_auth
@require_role([UserRole.MODERATOR, UserRole.ADMIN])
def update_delete_post_report(report_id, authenticated_user_id):
    post_report = PostReport.query.get_or_404(report_id)

    if request.method == "PUT":
        data = request.get_json()
        post_report.update(data)
        return post_report_schema.jsonify(post_report), 200

    elif request.method == "DELETE":
        post_report.delete()
        return jsonify({"message": "Report deleted successfully"}), 204
