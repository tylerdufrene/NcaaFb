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

api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))

def get_game_schedule(year=datetime.now().year,week=None):
    df = pd.DataFrame()
    try:
        games = api_instance.get_lines(year=year,week=week)
        for g in games:
            game_dict = {}
            game_dict['week_num'] = g.__getattribute__('week')
            game_dict['season'] = g.__getattribute__('season')
            game_dict['season_type'] = g.__getattribute__('season_type')
            game_dict['home_team'] = g.__getattribute__('home_team')
            game_dict['away_team'] = g.__getattribute__('away_team')
            game_dict['id'] = g.__getattribute__('id')
            game_df = pd.DataFrame([game_dict])
            df = pd.concat([df, game_df], axis=0)
    except ApiException as e:
        print(f"Exception when calling TeamsApi: {e}")
    return df.drop_duplicates()
            