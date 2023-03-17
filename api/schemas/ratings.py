from marshmallow import Schema, fields, validate

class RatingSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    content_id = fields.Integer(required=True)
    rating = fields.Float(required=True, validate=validate.Range(min=0, max=5))
    review = fields.String(validate=validate.Length(max=500))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
