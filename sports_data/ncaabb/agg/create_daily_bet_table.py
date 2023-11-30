import pandas as pd 
import datetime
import sqlite3

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
# cursor = conn.cursor()

def daily_bets_query():
    query = ''
    with open(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\ncaabb\agg\daily_bet_list.sql','r') as file:
        for line in file.readlines():
            query += line
    return query

def run_daily_bets():
    df = pd.read_sql_query(daily_bets_query(),conn).drop_duplicates()
    df.to_sql('ncaab_current_day_bets_to_make',conn,if_exists='replace',index=False)
    
def get_ui_teams():
    q = '''select a.* from (
            select away_team from ncaab_betting_lines
            union ALL
            select home_team from ncaab_betting_lines
        ) a
        left join ncaab_teams_odds_mapping b on b."Betting teams" = a.away_team
        where b."Betting Teams" is null
        order by 1
        ;'''
    return pd.read_sql_query(q,conn)

def replace_mapping_table(file):
    df = pd.read_excel(file)
    df.to_sql('ncaab_teams_odds_mapping',conn,if_exists='replace',index=False)

if __name__ == '__main__':
    run_daily_bets()
    print(get_ui_teams())