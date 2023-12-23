from marshmallow import Schema, fields, validate

class CommentSchema(Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String(required=True)
    user_id = fields.Integer(required=True)
    post_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    text = fields.String(required=True)

class CommentUpdateSchema(Schema):
    content = fields.String(validate=validate.Length(min=1))
