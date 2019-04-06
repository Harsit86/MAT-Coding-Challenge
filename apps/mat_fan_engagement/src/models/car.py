from enum import Enum
from geopy import distance
from logger import get_logger


class CarStatusTypes(Enum):
    SPEED = 'SPEED'
    POSITION = 'POSITION'


log = get_logger(__file__)


class CarStatus(object):
    def __init__(self, car_coordinates):
        self._init_loc = (car_coordinates['location']['long'], car_coordinates['location']['lat'])
        self._init_timestamp = car_coordinates['timestamp']

        self._cur_timestamp = self._init_timestamp
        self._cur_loc = self._init_loc

        self._index = car_coordinates['carIndex']
        #self._distance_travelled = 0
        self._cur_speed = 0
        self._cur_position = None

    def _location_delta(self, new_loc):
        return distance.distance((new_loc['long'], new_loc['lat']), self._cur_loc)

    def _time_delta_in_seconds(self, new_timestamp):
        return abs(new_timestamp - self._cur_timestamp) / 1000.0

    def calc_speed_miles_per_hour(self, distance, time):
        return distance.miles / time * 3600.0

    def update_status(self, car_coordinates):
        if self._init_timestamp != car_coordinates['timestamp']:
            dist_travelled = self._location_delta(car_coordinates['location'])
            delta_t = self._time_delta_in_seconds(car_coordinates['timestamp'])
            self._cur_speed = self.calc_speed_miles_per_hour(dist_travelled, delta_t)
            #self._distance_travelled += dist_travelled.km
            #self._cur_loc = new_pos
            # TODO - get car's current position
        self._update_current_status(car_coordinates)

    def _update_current_status(self, car_coordinates):
        self._cur_timestamp = car_coordinates['timestamp']
        self._cur_loc = (car_coordinates['location']['long'], car_coordinates['location']['lat'])

    def _current_status(self, type, value):
        return {
            'timestamp': self._cur_timestamp,
            'carIndex': self._index,
            'type': type,
            'value': value,
        }

    def get_current_speed_status(self):
        return self._current_status('SPEED', round(self._cur_speed))

    def get_current_position_status(self):
        return self._current_status(CarStatusTypes.POSITION, self._cur_position)
