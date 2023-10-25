import pandas as pd 
import sqlite3
import time

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
cursor = conn.cursor()
query = 'select School, TeamLookup from ncaab_all_teams'
teams = pd.read_sql_query(query, conn)

def get_team_season_stats(team,season):
    cols = ['G', 'Date', 'Home_Away', 'Opp_team', 'W/L', 'Tm', 'Opp_points', 'FG',
       'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'TRB',
       'AST', 'STL', 'BLK', 'TOV', 'PF', 'Unnamed: 23_level_1', 'opp_FG', 'opp_FGA',
       'opp_FG%', 'opp_3P', 'opp_3PA', 'opp_3P%', 'opp_FT', 'opp_FTA', 'opp_FT%', 'opp_ORB', 'opp_TRB', 'opp_AST',
       'opp_STL', 'opp_BLK', 'opp_TOV', 'opp_PF']
    df = pd.read_html(f'https://www.sports-reference.com/cbb/schools/{team}/men/{season}-gamelogs.html')[0]
    df = df.droplevel(0,axis=1)
    df.columns = cols 
    df['Home_Away'] = df.Home_Away.apply(lambda s: 'N' if s =='N'
                                         else 'A' if s == '@' else 'H')
    df = df[(~df['G'].isna())&(df['G']!='G')]
    df['Win'] = df['W/L'].apply(lambda w: str(w).__contains__('W'))
    df['Season'] = season 
    df['Team'] = team
    return df 

def get_all_teams_season(season):
    all_stats = pd.DataFrame()
    for tl in teams.loc[:,'TeamLookup']:
        try:
            df = get_team_season_stats(tl,season)
            all_stats = pd.concat([all_stats,df])
        except:
            print('Error getting',tl)
        time.sleep(5)
    return all_stats
        