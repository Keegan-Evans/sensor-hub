import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect(os.path.join("/home", "beta", "sensor_data.db"))

# Define your query
query = "SELECT * FROM air_quality;"

# Execute the query and fetch the results into a pandas DataFrame
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Display the DataFrame
print(df)