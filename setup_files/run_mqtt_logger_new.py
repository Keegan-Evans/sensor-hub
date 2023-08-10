import paho.mqtt.client as mqtt
import sqlite3

db_fp = os.path.join("/", "home", "beta", "sensor_data.db")

class WriteSensorData:
    def __init__(self, db_cursor, topic, table, measurements):
        self.db_cursor = db_cursor
        self.table = table
        self.topic = topic
        self.measurements = measurements

    def write_to_db(self, message):
        self.db_cursor.execute("INSERT INTO self.table (self.topic, message) VALUES (?, ?)", (self.topic, message))


# SQLite function
def write_to_db(topic, message):
    conn = sqlite3.connect(db_fp)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data (topic, message) VALUES (?, ?)", (topic, message))
    conn.commit()
    conn.close()

# Callbacks for Paho
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")  # Subscribe to all topics

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic} Message: {str(msg.payload.decode())}")
    write_to_db(msg.topic, str(msg.payload.decode()))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect("YOUR_MQTT_BROKER_IP", 1883, 60)
client.loop_forever()
