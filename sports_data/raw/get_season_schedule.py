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

def get_calendar(year=datetime.now().year):
    df = pd.DataFrame()
    try:
        calendar = api_instance.get_calendar(year=year)
        for dt in calendar:
            dt_dict = {}
            dt_dict['week'] = dt.__getattribute__('week')
            dt_dict['season_type'] = dt.__getattribute__('season_type')
            dt_dict['first_game_start'] = dt.__getattribute__('first_game_start')
            dt_dict['last_game_start'] = dt.__getattribute__('last_game_start')
            dt_dict['year'] = dt.__getattribute__('season')
            calendar_df = pd.DataFrame([dt_dict])
            df = pd.concat([df, calendar_df], axis=0)
    except ApiException as e:
        print(f"Exception when calling TeamsApi: {e}")
    return df
            
        