import pandas as pd 
import sqlite3

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\ncaafb\sports_reference.db')
cursor = conn.cursor()

def query_db(table,year=None,week=None):
    if week:
        df = pd.read_sql_query(
            f'''
            select * from {table}
            where season={year}
            and week_num={week}
            ''', conn
        )
    elif year:
            df = pd.read_sql_query(
            f'''
            select * from {table}
            where season={year}
            ''', conn
        )
    else:
            df = pd.read_sql_query(
            f'''
            select * from {table}
            ''', conn
        )
    return df