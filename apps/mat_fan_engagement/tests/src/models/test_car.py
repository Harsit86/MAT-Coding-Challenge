from src.models.car import Car
from src.schemas.car_status import CarStatusTypes


def test_car_status_initial_status():
    coordinates = {
        'carIndex': 0,
        'location': {
            'lat': 52.06371964824748,
            'long': -1.0169126377630506},
        'timestamp': 1554565525039
    }

    car_status = Car(coordinates)
    car_status.update_status(coordinates)
    actual = car_status.get_current_position_status()

    expected = {
        'timestamp': coordinates['timestamp'],
        'carIndex': coordinates['carIndex'],
        'type': CarStatusTypes.POSITION.name,
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
    car_status = Car(coords1)
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
        'type': CarStatusTypes.SPEED.name,
        'value': 175
    }
    assert actual == expected


def test_car_status_updated_location_position_status():
    coords1 = {
        'carIndex': 0,
        'location': {
            'lat': 52.07640151591944,
            'long': -1.0184079172947025
        },
        'timestamp': 1554566859732
    }
    car_status = Car(coords1)
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
    car_status.current_position = 1
    actual = car_status.get_current_position_status()

    expected = {
        'carIndex': 0,
        'timestamp': coords2['timestamp'],
        'type': CarStatusTypes.POSITION.name,
        'value': 1
    }
    assert actual == expected
    assert car_status._cur_loc == (coords2['location']['long'], coords2['location']['lat'])
    assert car_status._cur_timestamp == coords2['timestamp']


def test_car_status_initial_position_None():
    coords1 = {
        'carIndex': 0,
        'location': {
            'lat': 52.07640151591944,
            'long': -1.0184079172947025
        },
        'timestamp': 1554566859732
    }
    car_status = Car(coords1)
    car_status.update_status(coords1)

    actual = car_status.get_current_position_status()

    expected = {
        'carIndex': 0,
        'timestamp': coords1['timestamp'],
        'type': CarStatusTypes.POSITION.name,
        'value': None
    }
    assert actual == expected


def test_car_status_initial_speed_zero():
    coords1 = {
        'carIndex': 0,
        'location': {
            'lat': 52.07640151591944,
            'long': -1.0184079172947025
        },
        'timestamp': 1554566859732
    }
    car_status = Car(coords1)
    car_status.update_status(coords1)

    actual = car_status.get_current_speed_status()

    expected = {
        'carIndex': 0,
        'timestamp': coords1['timestamp'],
        'type': CarStatusTypes.SPEED.name,
        'value': 0,
    }
    assert actual == expected
