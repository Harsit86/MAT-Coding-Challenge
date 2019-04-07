from src.schemas.car_status import CarStatusSchema


STATUS_SCHEMA = CarStatusSchema()


def test_car_status_schema_valid_data():
    data = {
        'timestamp': 1,
        'carIndex': 1,
        'type': 'POSITION',
        'value': 10
    }

    actual = STATUS_SCHEMA.dump(data)

    assert actual.errors == {}
    assert actual.data == data
