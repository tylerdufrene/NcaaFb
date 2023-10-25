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

api_instance = cfbd.RatingsApi(cfbd.ApiClient(configuration))

def get_elo_ratings(year=datetime.now().year,week=None):
    talent = api_instance.get_elo_ratings(year=year)
    df = pd.DataFrame()
    try:
        # Retrieve a list of college football teams
        for team in talent:
            team_dict = {}
            team_dict['team'] = team.__getattribute__('team')
            team_dict['season'] = year 
            team_dict['conference'] = team.__getattribute__('conference')
            team_dict['elo'] = team.__getattribute__('elo')
            team_df = pd.DataFrame([team_dict])
            df = pd.concat([df,team_df], axis=0)
    except ApiException as e:
        print(f"Exception when calling TeamsApi: {e}")
    return df.reset_index(drop=True)

def get_fpi_ratings(year=datetime.now().year,week=None):
    fpi = api_instance.get_fpi_ratings(year=year)
    df = pd.DataFrame()
    try:
        # Retrieve a list of college football teams
        for team in fpi:
            team_dict = {}
            team_dict['team'] = team.__getattribute__('team')
            team_dict['season'] = year 
            team_dict['conference'] = team.__getattribute__('conference')
            team_dict['fpi'] = team.__getattribute__('fpi')
            team_dict['offense_efficiency'] = team.__getattribute__('efficiencies').__getattribute__('offense')
            team_dict['defense_efficiency'] = team.__getattribute__('efficiencies').__getattribute__('defense')
            team_dict['overall_efficiency'] = team.__getattribute__('efficiencies').__getattribute__('overall')
            team_dict['average_win_probability'] = team.__getattribute__('resume_ranks').__getattribute__('average_win_probability')
            team_dict['fpi_rank'] = team.__getattribute__('resume_ranks').__getattribute__('fpi')
            team_dict['game_control'] = team.__getattribute__('resume_ranks').__getattribute__('game_control')
            team_dict['strength_of_schedule'] = team.__getattribute__('resume_ranks').__getattribute__('strength_of_schedule')
            team_df = pd.DataFrame([team_dict])
            df = pd.concat([df,team_df], axis=0)
    except ApiException as e:
        print(f"Exception when calling TeamsApi: {e}")
    return df.reset_index(drop=True)
    