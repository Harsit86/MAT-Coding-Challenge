from marshmallow import (
    Schema,
    fields,
)


class LocationSchema(Schema):
    lat = fields.Float(required=True)
    long = fields.Float(required=True)


class CarCoordinatesSchema(Schema):
    timestamp = fields.Integer(required=True)
    carIndex = fields.Integer(required=True)
    location = fields.Nested(LocationSchema, required=True)

