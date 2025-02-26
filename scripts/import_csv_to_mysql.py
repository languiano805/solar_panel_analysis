import mysql.connector
import pandas as pd
from config import DB_CONFIG #import credentials from config.py

#conenct to mysql workbench
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

#check to see if the connection is successful
if conn.is_connected():
    print("Connected to MySQL database")
