import pandas as pd 
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

api_instance = cfbd.MetricsApi(cfbd.ApiClient(configuration))

def get_win_prob(year=datetime.now().year,week=None):
    wp = api_instance.get_pregame_win_probabilities(year=year,week=week)
    df = pd.DataFrame()
    try:
        # Retrieve a list of college football teams
        for team in wp:
            team_dict = {}
            team_dict['season'] = team.__getattribute__('season')
            team_dict['week_num'] = team.__getattribute__('week')
            team_dict['id'] = team.__getattribute__('game_id')
            team_dict['home_team'] = team.__getattribute__('home_team')
            team_dict['away_team'] = team.__getattribute__('away_team')
            team_dict['spread'] = team.__getattribute__('spread')
            team_dict['home_win_prob'] = team.__getattribute__('home_win_prob')
            team_df = pd.DataFrame([team_dict])
            df = pd.concat([df,team_df], axis=0)
    except ApiException as e:
        print(f"Exception when calling TeamsApi: {e}")
    return df.reset_index(drop=True)