from marshmallow import (
    Schema,
    fields,
)


class EventsSchema(Schema):
    timestamp = fields.Integer(required=True)
    text = fields.String(required=True)