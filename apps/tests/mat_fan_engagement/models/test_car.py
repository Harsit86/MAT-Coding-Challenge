from src.models.car import (
    CarStatus,
    CarStatusTypes,
)


def test_car_status_initial_status():
    coordinates = {
        'carIndex': 0,
        'location': {
            'lat': 52.06371964824748,
            'long': -1.0169126377630506},
        'timestamp': 1554565525039
    }

    car_status = CarStatus(coordinates)
    car_status.update_status(coordinates)
    actual = car_status.get_current_position_status()

    expected = {
        'timestamp': coordinates['timestamp'],
        'carIndex': coordinates['carIndex'],
        'type': CarStatusTypes.POSITION,
        'value': None,
    }
    assert actual == expected


def test_car_status_updated_location_speed_status():
    coords1 = {
        'carIndex': 0,
        'location': {
            'lat': 52.07640151591944,
            'long': -1.0184079172947025
        },
        'timestamp': 1554566859732
    }
    car_status = CarStatus(coords1)
    car_status.update_status(coords1)

    coords2 = {
        'carIndex': 0,
        'location': {
            'lat': 52.07649426484038,
            'long': -1.0185149430328098
        },
        'timestamp': 1554566859933
    }
    car_status.update_status(coords2)
    actual = car_status.get_current_speed_status()

    expected = {
        'carIndex': 0,
        'timestamp': coords2['timestamp'],
        'type': CarStatusTypes.SPEED,
        'value': 281
    }
    assert actual == expected
