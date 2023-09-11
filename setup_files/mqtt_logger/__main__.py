from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from callbacks import on_connect, on_message, log_sensor_data

import paho.mqtt.client as mqtt
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
