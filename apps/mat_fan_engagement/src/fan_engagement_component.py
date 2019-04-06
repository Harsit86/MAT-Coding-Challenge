import json
from logger import get_logger
import paho.mqtt.client as mqtt


from src.models.car import CarStatus


log = get_logger(__file__)


class FanEngagementComponent(object):

    def __init__(self, host='localhost', port=1883):
        self._host = host
        self._port = port
        self._num_messages = 0
        self._client = None
        self._car_status = {}

    def run(self):
        self._client = mqtt.Client()
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._client.connect(self._host, self._port)
        log.info(f'Connected to broker on {self._host}:{self._port}')
        self._client.loop_forever()

    @staticmethod
    def _on_connect(client, _1, _2, _3):
        client.subscribe('carCoordinates')
        log.info('Subscribed to carCoordinates')

    def _on_message(self, client, _, msg):
        car_coords = json.loads(msg.payload)
        self._num_messages += 1
        if car_coords['carIndex'] == 0:
            print(car_coords)

        car_index = car_coords['carIndex']
        car_status = self._car_status.get(car_index, CarStatus(car_coords))
        car_status.update_status(car_coords, self._num_messages)

        car_events = {
            'timestamp': car_coords['timestamp'],
            'text': 'test'
        }

        client.publish('carStatus', json.dumps(car_status.get_current_status()))
        client.publish('events', json.dumps(car_events))
