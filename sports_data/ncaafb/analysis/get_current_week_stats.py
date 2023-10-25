import pandas as pd 
import sqlite3
from datetime import datetime
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
cursor = conn.cursor()

with open('current_week_pregame.sql', 'r') as sql_file:
    sql_query = sql_file.read()
    
df = pd.read_sql_query(sql_query, conn)

df.to_sql('ncaaf_current_week_stats',conn, if_exists='replace',index=False)
