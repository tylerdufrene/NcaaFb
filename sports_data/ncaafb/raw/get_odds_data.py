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

api_instance = cfbd.BettingApi(cfbd.ApiClient(configuration))

def get_odds(year=datetime.now().year, week=None):
    df = pd.DataFrame()
    try:
        games = api_instance.get_lines(year=year,week=week)
        for g in games:
            game_dict = {}
            game_dict['id'] = g.__getattribute__('id')
            game_dict['week_num'] = g.__getattribute__('week')
            game_dict['season'] = g.__getattribute__('season')
            game_dict['start_date'] = g.__getattribute__('start_date')
            game_dict['home_team'] = g.__getattribute__('home_team')
            game_dict['home_team_conference'] = g.__getattribute__('home_conference')
            game_dict['away_team'] = g.__getattribute__('away_team')
            game_dict['away_team_conference'] = g.__getattribute__('away_conference')
            if g.__getattribute__('lines'):
                line = g.__getattribute__('lines')[0]
                game_dict['away_moneyline'] = line.__getattribute__('away_moneyline')
                game_dict['home_moneyline'] = line.__getattribute__('home_moneyline')
                game_dict['spread'] = line.__getattribute__('spread')
                game_dict['spread_open'] = line.__getattribute__('spread_open')
                game_dict['formatted_spread'] = line.__getattribute__('formatted_spread')
                game_dict['over_under'] = line.__getattribute__('over_under')
                game_dict['over_under_open'] = line.__getattribute__('over_under_open')
            else:
                game_dict['away_moneyline'] = None
                game_dict['home_moneyline'] = None
                game_dict['spread'] = None
                game_dict['spread_open'] = None
                game_dict['formatted_spread'] = None
                game_dict['over_under'] = None
                game_dict['over_under_open'] = None
            game_dict['date_updated'] = datetime.today()
            game_df = pd.DataFrame([game_dict])
            df = pd.concat([df, game_df], axis=0)
    except ApiException as e:
        print(f"Exception when calling TeamsApi: {e}")
    return df.drop_duplicates()