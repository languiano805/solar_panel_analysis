import os
from sqlalchemy import create_engine
from pathlib import Path
import matplotlib.pyplot as plt

import pandas as pd
from config import DB_CONFIG  # import credentials from config.py

# Create the connection string
connection_string = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"

# Create the engine
mydb = create_engine(connection_string)

# Test the connection
print(mydb)  # Should print something like: Engine(mysql+pymysql://root:***@localhost/solar_project)

#aggregate data by day

#load data from MySQL
df = pd.read_sql("SELECT inverter_id, AVG(daily_yield) AS avg_daily_yield FROM power_output WHERE date_time BETWEEN '2020-05-15' AND '2020-06-17' AND plant_id= '4136001' GROUP BY inverter_id ORDER BY avg_daily_yield", con=mydb)
print(df)