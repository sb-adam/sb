from marshmallow import Schema, fields, validate

class ReplySchema(Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String(required=True, validate=validate.Length(max=500))
    user_id = fields.Integer(required=True)
    comment_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
