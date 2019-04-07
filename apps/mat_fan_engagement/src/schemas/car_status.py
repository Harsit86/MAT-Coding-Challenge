from enum import Enum
from marshmallow import (
    Schema,
    fields,
    validate,
)


class CarStatusTypes(Enum):
    SPEED = 'SPEED'
    POSITION = 'POSITION'


class CarStatusSchema(Schema):
    timestamp = fields.Integer(required=True)
    carIndex = fields.Integer(required=True)
    type = fields.String(required=True, validate=validate.OneOf(list(CarStatusTypes.__members__.keys())))
    value = fields.Integer(required=True)