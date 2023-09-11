from mqtt_logger.log_data import add_sensors_reading_record
from mqtt_logger.sensor_data_models import (
    Topic,
    Sensor,
    Measurement,
    SensorMeasurement,
)
from importlib import resources
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import paho.mqtt.client as mqtt
import json
import sys
import os

Base = declarative_base()

with os.path.join("/", "home", "beta", "sensor_data.db") as sqlite_filepath:
    engine = create_engine(f"sqlite:///{sqlite_filepath}")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.commit()

client = mqtt.Client()
# Callbacks for Paho
def on_connect(client, userdata, flags, rc):
    """ "Generic on_connect function."""
    print("Connected with result code " + str(rc))
    client.subscribe("#")  # Subscribe to all topics


def on_message(client, userdata, msg):
    """Generic on_message function."""
    print(f"Topic: {msg.topic} Message: {str(msg.payload.decode())}")


def log_sensor_data(client, userdata, msg):
    """Provides callback for logging sensor_data."""
    session = session
    topic = msg.topic
    parsed_packet = json.loads(msg.payload.decode("utf-8"))
    measurements = parsed_packet["data"]
    sensor = parsed_packet["sensor"]
    print(f"Topic: {msg.topic} Message: {str(msg.payload.decode())}")
    add_sensors_reading_record(
        session=session, measurements=measurements, sensor=sensor, topic=topic
    )


client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add("sensor_data/#", log_sensor_data)

# Connect to MQTT broker
try:
    client.connect("localhost", 1883, 60)
except ConnectionRefusedError:
    print("MQTT broker not running")
    sys.exit(1)

client.loop_forever()


if __name__ == "__main__":
    main()
