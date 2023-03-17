from marshmallow import Schema, fields, validate

class ProfileBaseSchema(Schema):
    bio = fields.Str(validate=validate.Length(max=500))
    location = fields.Str(validate=validate.Length(max=100))
    website = fields.Str(validate=validate.Length(max=100))

class ProfileCreateSchema(ProfileBaseSchema):
    pass

class ProfileUpdateSchema(ProfileBaseSchema):
    pass

class ProfileSchema(ProfileBaseSchema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
