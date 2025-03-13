from pathlib import Path
from sqlalchemy import create_engine
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

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
WHERE p.plant_id  = '4135001'
"""
df = pd.read_sql(query, conn)

# close the connection
conn.close()

# convert date_time to dateimte format
df['date_time'] = pd.to_datetime(df['date_time'])

# set date_time as the index
df.set_index('date_time', inplace=True)

# group by week ,plant_id, and inverter_id and calculate metrics
weekly_data = df.resample('W').agg({
    'dc_power': 'mean',
    'ac_power': 'mean',
    'daily_yield': 'mean',
    'total_yield': 'sum',
    'ambient_temperature': 'mean',
    'module_temperature': 'mean',
    'irradiation': 'mean'
})

# add week column for clarity start week from 1
weekly_data['week'] = weekly_data.index.isocalendar().week

# show the processed data
print(weekly_data)

# create correlation heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(weekly_data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap of Weekly Data')
plt.tight_layout()


# save the png to folder output2
output_folder = Path('output2')
output_folder.mkdir(exist_ok=True)
plt.savefig(output_folder / 'weekly_data_correlation_heatmap.png')

plt.show()

# graph daily yield over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=weekly_data, x='week', y='daily_yield', marker='o')
plt.title('Daily Yield Over Time')
plt.xlabel('Week')
plt.ylabel('Daily Yield (kWh)')
plt.xticks(rotation=45)
plt.tight_layout()


# save png to folder output2
output_folder = Path('output2')
output_folder.mkdir(exist_ok=True)
plt.savefig(output_folder / 'daily_yield_over_time.png')


plt.show()

# graph module temperature over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=weekly_data, x='week', y='module_temperature', marker='o')
plt.title('Module Temperature Over Time ')
plt.xlabel('Week')
plt.ylabel('Module Temperature (°C)')
plt.xticks(rotation=45)
plt.tight_layout()

# save png to folder output2
output_folder = Path('output2')
output_folder.mkdir(exist_ok=True)
plt.savefig(output_folder / 'module_temperature_over_time.png')


plt.show()

# graph ambient temperature over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=weekly_data, x='week', y='ambient_temperature', marker='o')
plt.title('Ambient Temperature Over Time (week 24 removed)')
plt.xlabel('Week')
plt.ylabel('Ambient Temperature (°C)')
plt.xticks(rotation=45)
plt.tight_layout()


plt.show()
