from marshmallow import Schema, fields

class UserSchema(Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    phone_number = fields.Str(required=True)
