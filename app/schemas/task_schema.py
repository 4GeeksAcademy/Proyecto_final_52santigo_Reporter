from marshmallow import Schema, fields

class TaskSchema(Schema):
    title = fields.Str(required=True, validate=lambda x: len(x) > 0)
    description = fields.Str(required=True, validate=lambda x: len(x) > 0)
    countdown = fields.Int(required=True, validate=lambda x: x > 0)
    message = fields.Str(required=True, validate=lambda x: len(x) > 0)
    user_id = fields.Int(required=True)
