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

#get the average daily yield of the table
avg_daily_yield = df['avg_daily_yield'].mean()
print(f"Average daily yield: {avg_daily_yield}")
#find the standard deviation of the daily yield
std_dev = df['avg_daily_yield'].std()
print(f"Standard deviation: {std_dev}")
# Create a mapping of inverter_id to a simple index
inverter_mapping = {inv: idx for idx, inv in enumerate(df['inverter_id'].unique(), start=1)}

#find the inverters that are underperforming
underperforming_inverters = df[df['avg_daily_yield'] < avg_daily_yield - std_dev]
print("Underperforming inverters:")
print(underperforming_inverters)
# Plot the data

# Replace inverter_id with numeric labels in the dataframe
df['inverter_num'] = df['inverter_id'].map(inverter_mapping)

# Now plot using inverter_num instead of inverter_id
plt.figure(figsize=(10, 6))
plt.bar(df['inverter_num'], df['avg_daily_yield'])
plt.axhline(y=avg_daily_yield, color='r', linestyle='-')
plt.axhline(y=avg_daily_yield - std_dev, color='g', linestyle='-')
plt.axhline(y=avg_daily_yield + std_dev, color='g', linestyle='-')
plt.xlabel('Inverter (Assigned Number)')
plt.ylabel('Average Daily Yield (kWh)')
plt.title('Average Daily Yield of Inverters Plant 2')


#save the plot before showing it
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / "average_daily_yield2.png")

plt.show()


#save the underperforming inverters to a csv file
underperforming_inverters.to_csv(output_dir / "underperforming_inverters2.csv", index=False)

#check if the file was created
print(f"Underperforming inverters saved to {output_dir / 'underperforming_inverters2.csv'}")
#check if the plot was created
print(f"Plot saved to {output_dir / 'average_daily_yield2.png'}")
#close the connection
mydb.dispose()
#close the plot
plt.close()





