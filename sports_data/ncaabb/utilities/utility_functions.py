import pandas as pd 
import sqlite3
from datetime import datetime 

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
cursor = conn.cursor()

def data_exists(table, season=None):
    table_exists = False
    try:
        if season:
            q = pd.read_sql_query(f'select * from {table} where season={season} limit 10',conn)
        if len(q) > 1:
            table_exists = True 
    except:
        pass
    return table_exists 

def delete_statement(table, season=None):
    if season:
                return f'''
            DELETE FROM {table}
            where season = {season}
            '''
    else:
        return f'''
                DROP TABLE IF EXISTS {table}
                '''
                
def general_stats_2_db(fn, table,season=datetime.now().year):
    if data_exists(table,season):
        cursor.execute(delete_statement(table,season))
    fn(season).to_sql(table,if_exists='append',index=False,con=conn)
    