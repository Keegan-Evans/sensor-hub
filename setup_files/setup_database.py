import os
import sqlite3

# TODO refactor to single location
db_fp = os.path.join("/home", "beta", "sensor_data.db")

con = sqlite3.connect(db_fp)
cur = con.cursor()

try:
    cur.execute("CREATE TABLE air_quality (id INTEGER PRIMARY KEY, timestamp INTEGER, " \
        "sensor_id TEXT, co2 INTEGER, tvoc INTEGER, h2 INTEGER, ethanol INTEGER);")
    con.commit()
except sqlite3.OperationalError:
    pass
