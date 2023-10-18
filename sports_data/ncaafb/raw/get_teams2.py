import cfbd
import time 
from cfbd.rest import ApiException
from pprint import pprint
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)


import utilities.config as config
import pandas as pd

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = config.get_constants('API_KEY')

api_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))

def get_all_teams():
    df = pd.DataFrame()
    try:
        # Retrieve a list of college football teams
        teams = api_instance.get_teams()
        for team in teams:
            team_dict = {}
            team_dict['team_abbreviation'] = team.__getattribute__('abbreviation')
            team_dict['classification'] = team.__getattribute__('classification')
            team_dict['conference'] = team.__getattribute__('conference')
            team_dict['division'] = team.__getattribute__('division')
            team_dict['id'] = team.__getattribute__('id')
            team_dict['location_capacity'] = team.__getattribute__('location').__getattribute__('capacity')
            team_dict['location_city'] = team.__getattribute__('location').__getattribute__('city')                                                                                    
            team_dict['location_dome'] = team.__getattribute__('location').__getattribute__('dome')
            team_dict['location_elevation'] = team.__getattribute__('location').__getattribute__('elevation')
            team_dict['location_grass'] = team.__getattribute__('location').__getattribute__('grass')
            team_dict['location_latitude'] = team.__getattribute__('location').__getattribute__('latitude')
            team_dict['location_longitude'] = team.__getattribute__('location').__getattribute__('longitude')
            team_dict['location_name'] = team.__getattribute__('location').__getattribute__('name')
            team_dict['location_timezone'] = team.__getattribute__('location').__getattribute__('timezone')
            team_dict['location_year_constructed'] = team.__getattribute__('location').__getattribute__('year_constructed')
            team_dict['location_zip'] = team.__getattribute__('location').__getattribute__('zip')
            team_dict['school'] = team.__getattribute__('school')
            team_dict['twitter'] = team.__getattribute__('twitter')
            team_df = pd.DataFrame([team_dict])
            df = pd.concat([df,team_df], axis=0)
    except ApiException as e:
        print(f"Exception when calling TeamsApi: {e}")
    return df[~df['team_abbreviation'].isna()]