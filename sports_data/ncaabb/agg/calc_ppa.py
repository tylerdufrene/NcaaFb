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

def get_ppa():
    query = '''
            select 
            season, 
            avg(ortg) as PPa

            from ncaab_all_games_by_season_adv
            group by 1
            '''
    df = pd.read_sql_query(query,conn)
    df.to_sql('ncaab_ppa_by_season', conn, if_exists='replace',
              index=False)
    try:
        test = pd.read_sql_query('select 1 from ncaab_ppa_by_season', conn)
        print('Table Successfully created')
    except e:
        print('Table Failed')
        print(e)