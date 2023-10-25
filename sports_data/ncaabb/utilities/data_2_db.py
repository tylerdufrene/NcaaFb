import pandas as pd 
import sqlite3
from datetime import datetime
import os
import sys
from utility_functions import general_stats_2_db

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
# cursor = conn.cursor()

from raw.get_teams import get_teams
from raw.get_games import get_all_teams_season

def teams_2_db():
    get_teams().to_sql('ncaab_all_teams', conn, if_exists='replace', index=False)

def team_season_2_db(season):
    general_stats_2_db(get_all_teams_season, 'ncaab_all_games_by_season',season)