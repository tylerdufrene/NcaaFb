import pandas as pd 
import sqlite3
from datetime import datetime
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import utilities.config as config

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = config.get_constants('API_KEY')

api_instance = cfbd.StatsApi(cfbd.ApiClient(configuration))

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')

teams = pd.read_sql_query("""
                          select school from ncaaf_all_teams 
                          where classification in ('fbs','fcs')""", conn)

def get_team_stats(year=datetime.now().year,week_num=None):
    df = pd.DataFrame()
    try:
        # Retrieve a list of college football teams
        for team in teams.values:
            print(team[0])
            stats = api_instance.get_team_season_stats(team=team[0],year=year,start_week=week_num,
                                                       end_week=week_num)
            stats_dict = {}
            for stat in stats:
                stats_dict[stat.__getattribute__('stat_name')] = stat.__getattribute__('stat_value')

            stats_df = pd.DataFrame([stats_dict])
            stats_df['team'] = team[0]
            stats_df['season'] = year 
            stats_df['week_num'] = week_num
            df = pd.concat([df,stats_df], axis=0)
    except ApiException as e:
        print(f"Exception when calling TeamsApi: {e}")
    df = df.fillna(0)
    return df[df['games']==1]
        
