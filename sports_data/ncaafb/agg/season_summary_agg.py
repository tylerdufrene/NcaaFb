import pandas as pd 
import sqlite3
from datetime import datetime
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from utilities.utility_functions import query_db


columns = open('team_stats_column_order.txt').read().replace('\n','').split(',')
columns = [i.strip() for i in columns]

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\ncaafb\sports_reference.db')
cursor = conn.cursor()

def base_lead_table(year=datetime.now().year, week=None):
    grouped_cols = ['team_team','team_id','team_conference','week_num','id']
    rem_columns = [col for col in columns if col not in grouped_cols]
    lag_prefix = [f'lag({col},1,0) over (partition by team_id, season order by id) as {col}'
                  for col in rem_columns]
    if week:
        query = f'''
        select 
        {', '.join(grouped_cols)}
        , {', '.join(lag_prefix)}
        from ncaaf_game_stats_by_team
        where season = {year}
        and week_num = {week}
        '''
    else:
        query = f'''
        select 
        {', '.join(grouped_cols)}
        , {', '.join(lag_prefix)}
        from ncaaf_game_stats_by_team
        where season = {year}
        '''
    return query
        
    


# def create_partition_query(year=datetime.now().year, week=None, partition=None):
#     df1 = query_db('ncaaf_game_stats_by_team', year, week)
#     grouped_cols = ['team_team','team_id','team_conference','week_num','id']
#     rem_columns = [col for col in columns if col not in grouped_cols]
#
#     if partition:
#
#     query = f'''
#     select
#     {', '.join(grouped_cols)}
#     ,
#     {}
#     from ncaaf_game_stats_by_team
#     '''
    
    
    
    

    