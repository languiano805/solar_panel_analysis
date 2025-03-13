from pathlib import Path
from sqlalchemy import create_engine
import mysql.connector
import matplotlib.pyplot as plt


import pandas as pd
from config import DB_CONFIG  # import credentials from config.py

# create the connection string
conn = mysql.connector.connect(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database']
)


# agreate date by splitting the 30 days into 4 weeks
query = """
SELECT 
    p.date_time,
    p.plant_id,
    p.inverter_id,
    p.dc_power,
    p.ac_power,
    p.daily_yield,
    p.total_yield,
    w.ambient_temperature,
    w.module_temperature,
    w.irradiation
FROM power_output p
JOIN weather_sensors w
    USING(plant_id, date_time)
WHERE p.plant_id  = '4136001'
"""
df = pd.read_sql(query, conn)

# close the connection
conn.close()

#convert date_time to dateimte format
df['date_time'] = pd.to_datetime(df['date_time'])

#set date_time as the index
df.set_index('date_time', inplace=True)

#group by week ,plant_id, and inverter_id and calculate metrics 
weekly_data = df.resample('W').agg({
    'dc_power': 'mean',
    'ac_power': 'mean',
    'daily_yield': 'mean',
    'total_yield': 'sum',
    'ambient_temperature': 'mean',
    'module_temperature': 'mean',
    'irradiation': 'mean'
})

#add week column for clarity
weekly_data['week'] = weekly_data.index.isocalendar().week

#show the processed data
print(weekly_data)


# Plot dc_power over time
plt.figure(figsize=(10, 6))
plt.plot(weekly_data.index, weekly_data['dc_power'], label='DC Power (Average)', color='blue')
plt.xlabel('Date')
plt.ylabel('Average DC Power (kW)')
plt.title('Weekly Average DC Power Over Time')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)  # Rotate the x-axis labels for readability
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

# Plot multiple metrics
plt.plot(weekly_data.index, weekly_data['dc_power'], label='DC Power (Average)', color='blue')
plt.plot(weekly_data.index, weekly_data['ac_power'], label='AC Power (Average)', color='orange')
plt.plot(weekly_data.index, weekly_data['daily_yield'], label='Daily Yield (Average)', color='green')

# Labels and title
plt.xlabel('Date')
plt.ylabel('Power / Yield')
plt.title('DC Power, AC Power, and Daily Yield Over Time')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

import seaborn as sns

# Calculate the correlation matrix
corr = weekly_data[['dc_power', 'ac_power', 'daily_yield', 'ambient_temperature', 'module_temperature', 'irradiation']].corr()

# Create the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
plt.title('Correlation Heatmap of Performance and Weather Metrics')
plt.tight_layout()
plt.show()
