import pandas as pd 
import sqlite3
from datetime import datetime
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from utilities.utility_functions import query_db

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
cursor = conn.cursor()

def dissect_game_stats_table(year=datetime.now().year, week=None):
    df = query_db('ncaaf_game_stats_formatted',year,week)
    all_cols = ['week_num','season','id']
    home_cols = [col for col in df.columns if col.startswith('home_')] + all_cols
    away_cols = [col for col in df.columns if col.startswith('away_')] + all_cols
    return df[home_cols], df[away_cols]

def team_season_summary(dfa, dfb):
    df1, df2 = dfa.copy(), dfb.copy()
    df1.columns = [col.replace('home_','team_') if col.startswith('home_')
                   else col.replace('away_','team_') for col in df1.columns]
    df2.columns = [col.replace('home_','opponent_') if col.startswith('home_')
                   else col.replace('away_','opponent_') for col in df2.columns]
    df1_column_order = ['team_team','team_id','week_num','season','id'] + [col for col in df1.columns if col not in ['team_team','team_id','week_num','season','id']]
    df2['game_id'] = df2['id']
    df2_column_order = [col for col in df2.columns if col not in ['week_num','season','id']]
    df1 = df1[df1_column_order]
    df2 = df2[df2_column_order]
    return df1.merge(df2, how='inner',left_on='id',right_on='game_id').drop_duplicates().reset_index(drop=True)

def get_home_and_away_stats(year=None, week=None):
    home,away = dissect_game_stats_table(year,week)
    home_team = team_season_summary(home,away)
    away_team = team_season_summary(away,home)
    df = pd.concat([home_team, away_team])
    return df.drop_duplicates().reset_index(drop=True)