from marshmallow import Schema, fields

class FollowerSchema(Schema):
    id = fields.Integer(dump_only=True)
    follower_id = fields.Integer(required=True)
    following_id = fields.Integer(required=True)
