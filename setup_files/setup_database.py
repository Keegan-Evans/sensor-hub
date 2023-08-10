import os
import sqlite3

# TODO refactor to single location
db_fp = os.path.join("/home", "beta", "sensor_data.db")

con = sqlite3.connect(db_fp)
cur = con.cursor()

# setup air_quality table
try:
    cur.execute("CREATE TABLE air_quality (id INTEGER PRIMARY KEY, timestamp INTEGER, " \
        "sensor_id TEXT, co2 INTEGER, tvoc INTEGER, h2 INTEGER, ethanol INTEGER);")
    con.commit()
except sqlite3.OperationalError:
    pass

# setup weather_station table
try:
    cur.execute("CREATE TABLE weather_station (id INTEGER PRIMARY KEY, timestamp INTEGER, " \
        "sensor_id TEXT, wind_direction REAL, wind_speed REAL, rainfall REAL);")
    con.commit()
except sqlite3.OperationalError:
    pass

# setup soil_moisture table
try:
    cur.execute("CREATE TABLE soil_moisture (id INTEGER PRIMARY KEY, timestamp INTEGER, " \
        "sensor_id TEXT, moisture REAL);")
    con.commit()    
except sqlite3.OperationalError:
    pass