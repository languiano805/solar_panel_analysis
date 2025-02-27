import os
from pathlib import Path
import mysql.connector


import pandas as pd
from config import DB_CONFIG  # import credentials from config.py

# conenct to mysql workbench
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# check to see if the connection is successful
if conn.is_connected():
    print("Connected to MySQL database")


def import_csv(file_path, table_name, columns):
    df = pd.read_csv(file_path)

    # Standardize column names (convert to lowercase to match MySQL)
    # Strips spaces and converts to lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Convert 'date_time' column format using automatic inference
    df['date_time'] = pd.to_datetime(
        df['date_time'], errors='coerce')  # Automatically infers format
    df['date_time'] = df['date_time'].dt.strftime(
        '%Y-%m-%d %H:%M:%S')  # MySQL format

    # Convert DataFrame rows into list of tuples
    data = [tuple(row) for row in df.itertuples(index=False, name=None)]

    # Create SQL query with explicit column names
    # Creates placeholders like '%s, %s, %s'
    placeholders = ", ".join(["%s"] * len(columns))

    query = f"INSERT IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    # Insert data into MySQL
    cursor.executemany(query, data)
    conn.commit()


# Define columns for each table
power_columns = ["date_time", "plant_id", "source_key", "dc_power",
                 "ac_power", "daily_yield", "total_yield"]
weather_columns = ["date_time", "plant_id", "source_key",
                   "ambient_temperature", "module_temperature", "irradiation"]

# Import power generation data
try:
    import_csv("data/Plant_1_Generation_Data.csv",
               "power_output", power_columns)

    import_csv("data/Plant_2_Generation_Data.csv",
               "power_output", power_columns)
except mysql.connector.Error as err:
    print(f"Error: {err}")


# Import weather sensor data

try:
    import_csv("data/Plant_1_Weather_Sensor_Data.csv",
               "weather_sensors", weather_columns)

    import_csv("data/Plant_2_Weather_Sensor_Data.csv",
               "weather_sensors", weather_columns)
except mysql.connector.Error as err:
    print(f"Error: {err}")

cursor.close()
conn.close()
