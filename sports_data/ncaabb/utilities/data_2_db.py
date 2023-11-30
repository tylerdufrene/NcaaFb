import pandas as pd 
import sqlite3
from datetime import datetime
import os
import sys
from utility_functions import general_stats_2_db

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from agg.calc_ppa import get_ppa

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
# cursor = conn.cursor()

from raw.get_teams import get_teams
from raw.get_games import get_all_teams_season, get_all_games_advanced
from raw.get_betting_lines import get_espn_odds
from raw.get_todays_games import final_to_db

def teams_2_db():
    get_teams().to_sql('ncaab_all_teams', conn, if_exists='replace', index=False)

def team_season_2_db(season):
    general_stats_2_db(get_all_teams_season, 'ncaab_all_games_by_season',season)
    
def team_season_adv_2_db(season):
    general_stats_2_db(get_all_games_advanced, 'ncaab_all_games_by_season_adv',season)

def calc_ppa_by_season():
    get_ppa()
    
def todays_predictions():
    final_to_db()
    
def get_betting_lines():
    odds = get_espn_odds()
    print(odds)
    odds.to_sql('ncaab_betting_lines',conn,if_exists='replace',index=False)
    odds.to_sql('ncaab_betting_lines_historic',conn,if_exists='append',index=False)
    
    
if __name__ == '__main__':
    todays_predictions()
    get_betting_lines()