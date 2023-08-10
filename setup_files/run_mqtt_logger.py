import paho.mqtt.client as mqtt
import sqlite3
import json
import sys
import os

# TODO: implement try/except for all db operations so that good error messages are emitted

db_fp = os.path.join("/", "home", "beta", "sensor_data.db")

# Save abstraction for later
# class WriteSensorData:
    # def __init__(self, db_cursor, topic, table, measurements):
        # self.db_cursor = db_cursor
        # self.table = table
        # self.topic = topic
        # self.measurements = measurements
# 
    # def write_to_db(self, message):
        # self.db_cursor.execute("INSERT INTO self.table (self.topic, message) VALUES (?, ?)", (self.topic, message))

# def write_to_db(topic, message):
    # conn = sqlite3.connect(db_fp)
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO sensor_data (topic, message) VALUES (?, ?)", (topic, message))
    # conn.commit()
    # conn.close()

# Topic specific callback functions

# air_quality
def log_air_quality(client, userdata, message):
    parsed_packet = json.loads(message.payload.decode('utf-8'))
    aq_packet = {}
    aq_packet['timestamp'] = message.timestamp

    for k, v in parsed_packet['data'].items():
        aq_packet[k] = v

    aq_packet['sensor_id'] = parsed_packet['sensor']

    cursor.execute("INSERT INTO air_quality (id, co2, tvoc, h2, ethanol, sensor_id, timestamp) VALUES (NULL, :co2, :tvoc, :h2, :ethanol, :sensor_id, :timestamp)", aq_packet)
    conn.commit()
    sys.stdout.write("aq packet written to db\n")
    sys.stdout.flush()

# weather_station
def log_weather_station(client, userdata, message):
    parsed_packet = json.loads(message.payload.decode('utf-8'))
    ws_packet = {}
    ws_packet['timestamp'] = message.timestamp

    for k, v in parsed_packet['data'].items():
        ws_packet[k] = v

    ws_packet['sensor_id'] = parsed_packet['sensor']

    cursor.execute("INSERT INTO weather_station (id, wind_direction, wind_speed, rainfall, sensor_id, timestamp) VALUES (NULL, :wind_direction, :wind_speed, :rainfall, :sensor_id, :timestamp)", ws_packet)
    conn.commit()

    sys.stdout.write("ws packet written to db\n")
    sys.stdout.flush()

# soil_moisture
def log_soil_moisture(client, userdata, message):
    parsed_packet = json.loads(message.payload.decode('utf-8'))
    sm_packet = {}
    sm_packet['timestamp'] = message.timestamp

    for k, v in parsed_packet['data'].items():
        sm_packet[k] = v

    sm_packet['sensor_id'] = parsed_packet['sensor']

    cursor.execute("INSERT INTO soil_moisture (id, moisture, sensor_id, timestamp) VALUES (NULL, :moisture, :sensor_id, :timestamp)", sm_packet)
    conn.commit()

    sys.stdout.write("sm packet written to db\n")
    sys.stdout.flush()

# Callbacks for Paho
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")  # Subscribe to all topics

# the on_message callback function handles general sensor data packets, specific topic are handled by their own message_callback_add functions
def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic} Message: {str(msg.payload.decode())}")

conn = sqlite3.connect(db_fp)
cursor = conn.cursor()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add("sensor_data/air_quality", log_air_quality)
client.message_callback_add("sensor_data/weather_station", log_weather_station)
client.message_callback_add("sensor_data/soil_moisture", log_soil_moisture)

# Connect to MQTT broker
client.connect("10.42.0.1", 1883, 60)
client.loop_forever()