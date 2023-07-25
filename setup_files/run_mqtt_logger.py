import os
import json
import time
import sqlite3
import paho.mqtt.client as mqtt

# TODO refactor to single location
db_fp = os.path.join("/home", "beta", "sensor_data.db")

# log-parser function
def log_aq_data(database_connection, database_cursor, data: json):
    timestamp = time.time_ns()
    msg_data = json.loads(data)
    sensor = msg_data['sensor']
    co2 = msg_data['data']['co2']
    tvoc = msg_data['data']['tvoc']
    h2 = msg_data['data']['h2']
    ethanol = msg_data['data']['ethanol']
    #for measurement, val in msg_data['data'].items():
    #    var_name = str(measurement)
    #    var_name = int(val)


    database_cursor.execute("INSERT INTO air_quality VALUES "\
        "(?, ?, ?, ?, ?, ?);", (timestamp, sensor, co2, tvoc, h2, ethanol))

    database_connection.commit()

# database
con = sqlite3.connect(db_fp)
cur = con.cursor()

# callback functions for client

def on_connect(client, userdata, flags, rc):
    print("connected with code: {}".format(rc))
    client.subscribe("sensor_data/#")

def on_message(client, userdata, msg):
    topic_elements = msg.topic.split("/")
    #print(topic_elements)
    log_aq_data(con, cur, msg.payload)
    #print(msg.topic+" "+str(msg.payload))

# initialize mqtt
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("sensor_data/#")

# run client

try:
    client.loop_forever()
except:
    print("disconnecting from broker")

client.disconnect()
