import pandas as pd 
import datetime
import sqlite3

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
# cursor = conn.cursor()

def get_query(sql):
    query = ''
    with open(sql,'r') as file:
        for line in file.readlines():
            query += line
    return query

def run_query(sql, name):
    df = pd.read_sql_query(get_query(sql),conn).drop_duplicates()
    df.to_sql(name, conn, if_exists='replace',index=False)
    

if __name__ == '__main__':
    run_query(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\ncaabb\agg\ou_accuracy.sql', 'ncaab_ou_accuracy')
    run_query(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\ncaabb\agg\spread_accuracy.sql', 'ncaab_spread_accuracy')

    run_query(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\ncaabb\agg\ncaab_ou_daily_analysis.sql','NCAAB_OU_DAILY_ANALYSIS')
    run_query(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\ncaabb\agg\ncaab_spread_daily_analysis.sql','NCAAB_SPREAD_DAILY_ANALYSIS')
    
    run_query(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\ncaabb\agg\ou_historic_results.sql','ncaab_ou_historic_results')
    run_query(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\ncaabb\agg\ncaab_spread_historic_results.sql','ncaab_spread_historic_results')