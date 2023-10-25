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

api_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))

def get_talent_score(year=datetime.now().year,week=None):
    talent = api_instance.get_talent(year=year)
    df = pd.DataFrame()
    try:
        # Retrieve a list of college football teams
        for team in talent:
            team_dict = {}
            team_dict['team'] = team.__getattribute__('school')
            team_dict['season'] = year 
            team_dict['talent_score'] = team.__getattribute__('talent')
            team_df = pd.DataFrame([team_dict])
            df = pd.concat([df,team_df], axis=0)
    except ApiException as e:
        print(f"Exception when calling TeamsApi: {e}")
    return df.reset_index(drop=True)
    