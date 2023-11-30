import pandas as pd 
import datetime
import sqlite3
import json

# df = pd.read_csv('https://barttorvik.com/2024_super_sked.csv',header=None)

import requests

# url = 'https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=basketball&league=mens-college-basketball&region=us&lang=en&contentorigin=espn&buyWindow=1m&showAirings=buy%2Clive%2Creplay&showZipLookup=true&tz=America%2FNew_York'

# def get_espn_odds(url):
#     r = requests.get(url)
#     data = r.json()
#     games = data['sports'][0]['leagues'][0]['events']
#     df = pd.DataFrame()
#     for i in games[0]:
#         temp = pd.DataFrame()
#         temp['date'] = i['date']
#         temp['name'] = i['name']
#         temp['season'] = i['season']
#         for c in i['competitors']:
#             if c['homeAway'] == 'home':
#                 temp['home_team'] = c['displayName']
#                 temp['home_name'] = c['name']
#                 temp['home_abbr'] = c['abbreviation']
#             else:
#                 temp['away_team'] = c['displayName']
#                 temp['away_name'] = c['name']
#                 temp['away_abbr'] = c['abbreviation']
#         for o in i['odds']:
#             temp['fav'] = o['details']
#             temp['overUnder'] = o['overUnder']
#             temp['spread'] = o['spread']
#             temp['home_ml'] = o['home']['moneyLine']
#             temp['home_team_fav'] = o['homeTeamOdds']['favorite']
#             temp['home_team'] = o['homeTeamOdds']['team']['abbreviation']
#             temp['home_spread'] = o['pointSpread']['home']['closed']['line']
#             temp['away_ml'] = o['away']['moneyLine']
#             temp['away_team_fav'] = o['awayTeamOdds']['favorite']
#             temp['away_team'] = o['awayTeamOdds']['team']['abbreviation']
#             temp['away_spread'] = o['pointSpread']['away']['closed']['line']
#             temp['total'] = o['total']['over']['closed']['line']
#         df = pd.concat([df,temp])
#     return df


def get_espn_odds():
    url = 'https://www.espn.com/mens-college-basketball/lines'
    data = pd.read_html(url)

    df = pd.DataFrame()
    columns = ['away_team','away_record','line','away_ml','away_bpi',
               'home_team','home_record','spread','home_ml','home_bpi']
    # temp_columns = ['team','record','line','ml','bpi']
    for x in data:
        try:
            merged_df = pd.concat([x.iloc[0], x.iloc[1]], axis=0).to_frame().T
            merged_df.columns = columns
            df = pd.concat([df,merged_df])
        except:
            print(x, 'could not be appended')
    return df
        
    