from flask import Blueprint, request, jsonify
from ..models import Report, UserRole
from ..schemas import ReportSchema
from ..utils.auth import require_auth, require_role

reports_blueprint = Blueprint("reports", __name__)
report_schema = ReportSchema()

@reports_blueprint.route("/comments/<int:comment_id>/reports", methods=["POST"])
@require_auth
def create_report(comment_id, authenticated_user_id):
    data = request.get_json()
    report = Report(user_id=authenticated_user_id, comment_id=comment_id, reason=data["reason"])
    report.save()
    return report_schema.jsonify(report), 201

@reports_blueprint.route("/comments/<int:comment_id>/reports", methods=["GET"])
@require_auth
@require_role([UserRole.MODERATOR, UserRole.ADMIN])
def get_reports(comment_id, authenticated_user_id):
    reports = Report.query.filter_by(comment_id=comment_id).all()
    return report_schema.jsonify(reports, many=True), 200
