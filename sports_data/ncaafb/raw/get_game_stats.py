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

api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))


def get_game_stats(year=datetime.now().year,week_num=None):
    df = pd.DataFrame()
    try:
        game_stats = api_instance.get_team_game_stats(year=year,week=week_num)
        for game in game_stats:
            stats_dict = {}
            stats_dict['id'] = game.__getattribute__('id')
            for team in game.__getattribute__('teams'):
                if team.__getattribute__('home_away') == 'home':
                    stats_dict['home_team'] = team.__getattribute__('school')
                    stats_dict['home_conference'] = team.__getattribute__('conference')
                    stats_dict['home_id'] = team.__getattribute__('school_id')
                    stats_dict['home_points'] = team.__getattribute__('points')
                    for s in team.__getattribute__('stats'):
                        stats_dict['home_'+s.__getattribute__('category')] = s.__getattribute__('stat')
                else:
                    stats_dict['away_team'] = team.__getattribute__('school')
                    stats_dict['away_conference'] = team.__getattribute__('conference')
                    stats_dict['away_id'] = team.__getattribute__('school_id')
                    stats_dict['away_points'] = team.__getattribute__('points')
                    for s in team.__getattribute__('stats'):
                        stats_dict['away_'+s.__getattribute__('category')] = s.__getattribute__('stat')
            stats_df = pd.DataFrame([stats_dict])
            stats_df['season'] = year 
            stats_df['week_num'] = week_num
            stats_df = stats_df.sort_index(axis=1,ascending=False)
            df = pd.concat([df,stats_df], axis=0)
    except ApiException as e:
        print(f"Exception when calling TeamsApi: {e}")
    return df.drop_duplicates().fillna(0)
        
