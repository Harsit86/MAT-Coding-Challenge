import os
import numpy as np

from src.models.car import CarStatus


CAR_COUNT = os.environ.get('CAR_COUNT', 6)  # hard-code 6 for now


class Race(object):

    def __init__(self):
        self._cars = {}
        self._event = None
        self._timestamp = None
        self._car_positions = None

    def _update_car_status(self, car_coordinates):
        car_index = car_coordinates['carIndex']
        if car_index not in self._cars:
            car_status = CarStatus(car_coordinates)
            self._cars[car_index] = car_status

        self._cars[car_index].update_status(car_coordinates)

    def _set_event(self, car_positions, car_index):
        self._event = None
        if self._car_positions:
            new_pos = car_positions[car_index]
            prev_pos = self._car_positions[car_index]
            diff = prev_pos - new_pos
            if diff > 0:
                res = []
                for i, v in car_positions.items():
                    if new_pos < v <= prev_pos:
                        res.append(f'Car {i}')

                if len(res) > 1:
                    res = res[:-1] + [f'and {res[-1]}']

                self._event = f'Car {car_index} races ahead of {", ".join(res)} in a dramatic overtake.'

    def _update_car_positions(self, car_index):
        car_positions = self.get_car_positions()
        if car_positions is not None:
            self._cars[car_index].set_position(car_positions[car_index])
            self._set_event(car_positions, car_index)
            self._car_positions = car_positions

    def update_race_status(self, car_coordinates):
        self._timestamp = car_coordinates['timestamp']
        self._update_car_status(car_coordinates)
        self._update_car_positions(car_coordinates['carIndex'])

    def get_car_status(self, car_index):
        return [
            self._cars[car_index].get_current_speed_status(), self._cars[car_index].get_current_position_status()
        ]

    def get_event(self):
        if self._event:
            return {
                'timestamp': self._timestamp,
                'text': self._event,
            }
        else:
            return None

    def get_car_positions(self):
        if len(self._cars) == CAR_COUNT:
            car_distances = [self._cars[i].get_distance_travelled() for i in range(CAR_COUNT)]
            return dict(zip(np.argsort(car_distances)[::-1], range(CAR_COUNT)))

            # TODO - tidy up current code and write tests
            # TODO - schemas
            # TODO - update readme
            # TODO - dockerise
