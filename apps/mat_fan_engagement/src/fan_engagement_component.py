import json
from logger import get_logger
import paho.mqtt.client as mqtt


from src.models.race import Race


log = get_logger(__file__)


class FanEngagementComponent(object):

    def __init__(self, host='localhost', port=1883):
        self._host = host
        self._port = port
        self._client = None
        self._car_status = {}
        self._race = Race()

    def run(self):
        self._client = mqtt.Client()
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._client.connect(self._host, self._port)
        self._client.on_log = self._on_log
        log.info(f'Connected to broker on {self._host}:{self._port}')
        self._client.loop_forever()

    @staticmethod
    def _on_connect(client, _1, _2, _3):
        client.subscribe('carCoordinates')
        log.info('Subscribed to carCoordinates')

    @staticmethod
    def _on_log(_1, _2, _3, buf):
        log.info(str(buf))

    def _on_message(self, client, _, msg):
        car_coords = json.loads(msg.payload)
        self._race.update_race_status(car_coords)
        car_status = self._race.get_car_status(car_coords['carIndex'])
        event = self._race.get_event()

        client.publish('carStatus', json.dumps(car_status[0]))
        client.publish('carStatus', json.dumps(car_status[1]))
        if event is not None:
            client.publish('events', json.dumps(event))
