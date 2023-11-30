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

def create_stg_table(year=None):
    stg_file = ''
    for i in open('ncaab_stg_eff_calc.sql','r'):
        stg_file += i 
    stg = pd.read_sql_query(stg_file,conn)
    stg.to_sql('ncaab_stg_eff_calc', conn, if_exists='replace',
               index=False)