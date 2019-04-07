import pytest
from unittest import mock

from src.models.race import Race


MODULE_UNDER_TEST = Race.__module__


@mock.patch(f'{MODULE_UNDER_TEST}.CAR_COUNT', 2)
def test_race_two_cars_status_update_car0():
    car_coords = {
        'carIndex': 0,
        'location': {
            'lat': 52.06524277952301,
            'long': -1.0202423237779028
        },
        'timestamp': 1554655454219
    }
    race = Race()
    race.update_race_status(car_coords)

    car_status = race.get_car_status(car_coords['carIndex'])
    event = race.get_latest_event()

    assert event is None
    assert car_status == [{
        'timestamp': car_coords['timestamp'],
        'carIndex': car_coords['carIndex'],
        'type': 'SPEED',
        'value': 0
    }, {
        'timestamp': car_coords['timestamp'],
        'carIndex': car_coords['carIndex'],
        'type': 'POSITION',
        'value': None
    }]


@mock.patch(f'{MODULE_UNDER_TEST}.CAR_COUNT', 2)
def test_race_two_cars_status_update_car_not_in_race():
    car_coords = {
        'carIndex': 0,
        'location': {
            'lat': 52.06524277952301,
            'long': -1.0202423237779028
        },
        'timestamp': 1554655454219
    }
    race = Race()
    race.update_race_status(car_coords)

    with pytest.raises(KeyError):
        _ = race.get_car_status(2)


@mock.patch(f'{MODULE_UNDER_TEST}.CAR_COUNT', 2)
def test_race_two_cars_car_positons():
    race = Race()
    car_coords0 = {
        'carIndex': 0,
        'location': {
            'lat': 52.06524277952301,
            'long': -1.0202423237779028
        },
        'timestamp': 1554655454219
    }
    car_coords1 = {
        'carIndex': 1,
        'location': {
            'lat': 52.06775379019839,
            'long': -1.0240924037829002
        },
        'timestamp': 1554655462263

    }

    race.update_race_status(car_coords0)
    race.update_race_status(car_coords1)

    event = race.get_latest_event()
    actual = race.get_car_positions()
    assert event is None
    assert actual == {
        1: 0,
        0: 1
    }


@mock.patch(f'{MODULE_UNDER_TEST}.CAR_COUNT', 2)
def test_race_two_cars_event_car0_overtakes_car1():
    race = Race()
    car_coords0_0 = {
        'carIndex': 0,
        'location': {
            'lat': 52.06524277952301,
            'long': -1.0202423237779028
        },
        'timestamp': 1554655454219
    }
    car_coords1_0 = {
        'carIndex': 1,
        'location': {
            'lat': 52.06775379019839,
            'long': -1.0240924037829002
        },
        'timestamp': 1554655462263

    }
    car_coords0_1 = {
        'carIndex': 0,
        'location': {
            'lat': 52.06775379019839,
            'long': -1.0340924037829002,
        },
        'timestamp': 1554655462263
    }

    race.update_race_status(car_coords0_0)
    race.update_race_status(car_coords1_0)
    race.update_race_status(car_coords0_1)

    event = race.get_latest_event()
    actual = race.get_car_positions()
    assert event == {
        'timestamp': car_coords0_1['timestamp'],
        'text': 'Car 0 races ahead of Car(s) 1 in a dramatic overtake.'
    }
    assert actual == {
        0: 0,
        1: 1
    }
