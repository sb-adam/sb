from flask import Blueprint, request, jsonify
from ..models import Report, PostReport
from ..schemas import ReportSchema, PostReportSchema
from ..utils.auth import require_moderator

moderation_blueprint = Blueprint("moderation", __name__)
report_schema = ReportSchema()
post_report_schema = PostReportSchema()

@moderation_blueprint.route("/moderation", methods=["GET"])
@require_moderator
def get_pending_moderation_items(authenticated_user_id):
    pending_reports = Report.query.filter_by(status="pending").all()
    pending_post_reports = PostReport.query.filter_by(status="pending").all()
    result = {
        "reports": report_schema.dump(pending_reports, many=True),
        "post_reports": post_report_schema.dump(pending_post_reports, many=True),
    }
    return jsonify(result), 200

@moderation_blueprint.route("/moderation/<string:moderation_type>/<int:item_id>", methods=["PUT"])
@require_moderator
def update_moderation_status(moderation_type, item_id, authenticated_user_id):
    if moderation_type == "report":
        item = Report.query.get_or_404(item_id)
    elif moderation_type == "post_report":
        item = PostReport.query.get_or_404(item_id)
    else:
        return jsonify({"message": "Invalid moderation type"}), 400

    data = request.get_json()
    status = data.get("status")

    if status not in ["nothing", "delete", "banned"]:
        return jsonify({"message": "Invalid moderation status"}), 400

    item.update_status(status, authenticated_user_id)
    return jsonify({"message": "Moderation status updated"}), 200
