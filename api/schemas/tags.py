from marshmallow import Schema, fields, validate


class TagSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserTagSchema(Schema):
    tag_id = fields.Integer(required=True)
