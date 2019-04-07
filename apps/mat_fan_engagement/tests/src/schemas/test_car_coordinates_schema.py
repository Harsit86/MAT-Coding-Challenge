from src.schemas.car_coordinates import CarCoordinatesSchema


CC_SCHEMA = CarCoordinatesSchema()


def test_car_coordinates_schema_no_errors():
    car_coordinate = {
        "timestamp": 1541693114862,
        "carIndex": 2,
        "location": {
            "lat": 51.349937311969725,
            "long": -0.544958142167281
        }
    }

    actual = CC_SCHEMA.load(car_coordinate)

    assert actual.errors == {}
    assert actual.data == car_coordinate
