from marshmallow import Schema, fields, validate

class ReportSchema(Schema):
    id = fields.Integer(dump_only=True)
    reporter_id = fields.Integer(required=True)
    content_id = fields.Integer(required=True)
    content_type = fields.String(required=True, validate=validate.OneOf(['comment', 'post']))
    reason = fields.String(required=True)
    status = fields.String(dump_only=True, validate=validate.OneOf(['pending', 'resolved']), default='pending')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
