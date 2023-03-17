from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=[validate.Length(min=3)])
    email = fields.Email(required=True)
    # password = fields.Str(required=True, validate=[validate.Length(min=8)])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    # is_admin = fields.Boolean(dump_only=True)
