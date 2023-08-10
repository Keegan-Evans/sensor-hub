# imports for writing mqtt to sqlite db
import paho.mqtt.client as mqtt
import sqlite3
import os
import sys
import json
# define file path for sqlite db(sensor_data.db)
db_fp = os.path.join("/", "home", "beta", "sensor_data.db")

# setup connection and cursor for sqlite db
conn = sqlite3.connect(db_fp)
cursor = conn.cursor()

def on_message(client, userdata, msg):
    parse_message(msg)

def on_connect(client, userdata, flags, rc):
    client.subscribe("sensor_data/#")

# create an on_message callback function that writes mqtt messages to sqlite db, with each topic being written to a different table
# def on_message(client, userdata, msg):
# 
    # print(f"Topic: {msg.topic} Message: {str(msg.payload.decode())}")
    # cursor.execute("INSERT INTO sensor_data (topic, message) VALUES (?, ?)", (msg.topic, str(msg.payload.decode())))
    # conn.commit()

# function to parse value of data key in mqtt message into key-value pairs and use the keys to write values into sqlite db

def parse_air_quality(client, userdata, message):
    parsed_packet = json.loads(message.payload.decode('utf-8'))
    aq_packet = {}
    aq_packet['timestamp'] = message.timestamp
    for k, v in parsed_packet['data'].items():
        # sys.stdout.write(str(k) + str(v) + "\n")
        # sys.stdout.flush()
        aq_packet[k] = v
    aq_packet['sensor_id'] = parsed_packet['sensor']
        

# 
# 
    cursor.execute("INSERT INTO air_quality (id, co2, tvoc, h2, ethanol, sensor_id, timestamp) VALUES (NULL, :co2, :tvoc, :h2, :ethanol, :sensor_id, :timestamp)", aq_packet)
    conn.commit()
    sys.stdout.write("aq packet written to db\n")
    sys.stdout.flush()
        
# function to parse message and print to console
def parse_message(message):
    received_data = json.loads(message.payload)
    data = received_data['data']
    sensor = received_data['sensor']

    sys.stdout.write(str(received_data['data'].keys()))
    sys.stdout.write(str(message.topic) + str(json.loads(message.payload)) + "\n")
    sys.stdout.flush()

# create, setup, and connect to client object
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.message_callback_add("sensor_data/air_quality", parse_air_quality)

client.loop_forever()
