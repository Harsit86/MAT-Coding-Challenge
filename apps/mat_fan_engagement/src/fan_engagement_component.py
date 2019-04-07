import os
import json
from logger import get_logger
import paho.mqtt.client as mqtt


from src.models.race import Race


# hard-coded for now
CAR_COORDS_TOPIC = os.environ.get('MQTT_TOPIC', 'carCoordinates')
CAR_STATUS_TOPIC = os.environ.get('MQTT_STATUS_TOPIC', 'carStatus')
EVENTS_TOPIC = os.environ.get('MQTT_EVENTS_TOPIC', 'events')
log = get_logger(__file__)


class FanEngagementComponent(object):

    def __init__(self, host='localhost', port=1883):
        self._host = host
        self._port = port
        self._client = None
        self._race = Race()

    def run(self):
        self._client = mqtt.Client()
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._client.connect(self._host, self._port)
        self._client.enable_logger(log)
        self._client.on_log = self._on_log
        log.info(f'Connected to broker on {self._host}:{self._port}')
        self._client.loop_forever()

    @staticmethod
    def _on_connect(client, _1, _2, _3):
        client.subscribe(CAR_COORDS_TOPIC)
        log.info(f'Subscribed to {CAR_COORDS_TOPIC}.')

    @staticmethod
    def _on_log(_1, _, level, buf):
        if level < mqtt.MQTT_LOG_DEBUG:
            log.info(str(buf))

    def _on_message(self, client, _, msg):
        car_coords = json.loads(msg.payload)
        log.info(f'Received car coordinates: {json.dumps(car_coords)}.')

        self._race.update_race_status(car_coords)
        car_status = self._race.get_car_status(car_coords['carIndex'])
        client.publish(CAR_STATUS_TOPIC, json.dumps(car_status[0]))
        client.publish(CAR_STATUS_TOPIC, json.dumps(car_status[1]))
        log.info(f'Publishing car status: {json.dumps(car_status)}')

        event = self._race.get_latest_event()
        if event is not None:
            event = json.dumps(event)
            log.info(f'Published event: {event}')
            client.publish(EVENTS_TOPIC, event)
