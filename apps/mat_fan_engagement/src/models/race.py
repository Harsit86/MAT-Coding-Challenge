import os
import numpy as np

from src.models.car import Car


# hard-code 6 for now
CAR_COUNT = os.environ.get('CAR_COUNT', 6)


class Race(object):

    def __init__(self):
        self._cars = {}
        self._event = None
        self._timestamp = None
        self._car_positions = None

    def update_race_status(self, car_coordinates):
        self._timestamp = car_coordinates['timestamp']
        self._update_car_status(car_coordinates)
        self._update_car_positions(car_coordinates['carIndex'])

    def _update_car_status(self, car_coordinates):
        car_index = car_coordinates['carIndex']
        if car_index not in self._cars:
            car = Car(car_coordinates)
            self._cars[car_index] = car

        self._cars[car_index].update_status(car_coordinates)

    def _set_event(self, car_positions, car_index):
        self._event = None
        if self._car_positions:
            new_pos = car_positions[car_index]
            prev_pos = self._car_positions[car_index]
            if prev_pos > new_pos:
                cars_overtaken = map(
                    lambda y: str(y[0]),
                    filter(lambda x: new_pos < x[1] <= prev_pos, car_positions.items())
                )
                self._event = f'Car {car_index} races ahead of Car(s) {", ".join(cars_overtaken)} in a dramatic overtake.'

    def _update_car_positions(self, car_index):
        car_positions = self.get_car_positions()
        if car_positions is not None:
            self._cars[car_index].current_position = car_positions[car_index]
            self._set_event(car_positions, car_index)
            self._car_positions = car_positions

    def get_car_status(self, car_index):
        return [
            self._cars[car_index].get_current_speed_status(), self._cars[car_index].get_current_position_status()
        ]

    def get_latest_event(self):
        return None if not self._event else {'timestamp': self._timestamp, 'text': self._event}

    def get_car_positions(self):
        if len(self._cars) != CAR_COUNT:
            # Only calculate car positions once we have distance travelled for all cars
            return

        car_distances = [self._cars[i].distance_travelled for i in range(CAR_COUNT)]
        return dict(zip(np.argsort(car_distances)[::-1], range(CAR_COUNT)))
