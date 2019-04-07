import os
import json
from logger import get_logger
import paho.mqtt.client as mqtt

from src.schemas.car_coordinates import CarCoordinatesSchema
from src.schemas.car_status import CarStatusSchema
from src.schemas.events import EventsSchema
from src.models.race import Race


# hard-coded for now
CAR_COORDS_TOPIC = os.environ.get('MQTT_TOPIC', 'carCoordinates')
CAR_STATUS_TOPIC = os.environ.get('MQTT_STATUS_TOPIC', 'carStatus')
EVENTS_TOPIC = os.environ.get('MQTT_EVENTS_TOPIC', 'events')
CC_SCHEMA = CarCoordinatesSchema()
STATUS_SCHEMA = CarStatusSchema()
EVENTS_SCHEMA = EventsSchema()
log = get_logger(__file__)


class FanEngagementComponent(object):

    def __init__(self, host='localhost', port=1883):
        self._host = host
        self._port = port
        self._race = Race()

        self._client = mqtt.Client()
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._client.on_log = self._on_log

    def run(self):
        self._client.connect(self._host, self._port)
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

    @staticmethod
    def _valid_data(schema, data):
        result = schema.dump(data)
        if result.errors:
            log.error(f'Invalid data: {data}, errors: {result.errors}')

        return result.errors == {}

    def _validate_car_status_data_and_publish(self, client, data):
        if self._valid_data(STATUS_SCHEMA, data):
            client.publish(CAR_STATUS_TOPIC, json.dumps(data))
            log.info(f'Published car status: {data}')

    def _validate_event_data_and_publish(self, client):
        event = self._race.get_latest_event()
        if event is not None:
            if self._valid_data(EVENTS_SCHEMA, event):
                log.info(f'Published event: {event}')
                event = json.dumps(event)
                client.publish(EVENTS_TOPIC, event)

    def _on_message(self, client, _, msg):
        payload = json.loads(msg.payload)
        car_coords = CC_SCHEMA.load(payload)

        if car_coords.errors:
            log.error(f'Failed to process message: {payload}, errors: {car_coords.errors}.')

        else:
            log.info(f'Received car coordinates: {payload}.')

            # Update race status
            data = car_coords.data
            self._race.update_race_status(data)

            # get car status and publish messages
            car_status = self._race.get_car_status(data['carIndex'])
            self._validate_car_status_data_and_publish(client, car_status[0])
            self._validate_car_status_data_and_publish(client, car_status[1])

            # publish event
            self._validate_event_data_and_publish(client)