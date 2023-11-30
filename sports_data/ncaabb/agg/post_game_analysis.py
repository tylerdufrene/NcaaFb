import pandas as pd 
import datetime
import sqlite3

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
# cursor = conn.cursor()

def get_post_game_analysis():
    raw = pd.read_json('https://barttorvik.com/2024_super_sked.json')
    columns = ['muid', 'date', 'conmatch', 'matchup', 'prediction', 'ttq', 'conf', 'venue',
            'team1', 't1oe', 't1de', 't1py', 't1wp', 't1propt', 'team2', 't2oe', 't2de', 't2py', 't2wp',
            't2propt', 'tpro', 't1qual', 't2qual', 'gp', 'result', 'tempo', 'possessions', 't1pts',
            't2pts', 'winner', 'loser', 't1adjt', 't2adjt', 't1adjo', 't1adjd', 't2adjo', 't2adjd',
            'gamevalue', 'mismatch', 'blowout', 't1elite', 't2elite', 'ord_date', 't1ppp', 't2ppp', 'gameppp',
            't1rk', 't2rk', 't1gs', 't2gs', 'gamestats', 'overtimes', 't1fun', 't2fun', 'results']
    raw.columns = columns
    raw['date'] = pd.to_datetime(raw['date'], format='%m/%d/%y')
    to_date = raw[raw['gp']==1]
    df =  to_date[['date','matchup','team1','team2','t1propt','t2propt','result','t1pts','t2pts',
                   'winner','loser','t2fun']]
    return df.to_sql('ncaab_post_game_results',conn, if_exists='replace',index=False)

if __name__ == '__main__':
    get_post_game_analysis()