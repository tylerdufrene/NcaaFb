import pandas as pd 
import sqlite3
from datetime import datetime
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from utilities.utility_functions import query_db


columns = open(current_dir + r'\team_stats_column_order.txt').read().replace('\n','').split(',')
columns = [i.strip() for i in columns]

grouped_cols = ['team_team','team_id','team_conference','season','week_num','id']
rem_columns = [col for col in columns if col not in grouped_cols]
lag_prefix = [f'lag({col},1,0) over (partition by team_id, season order by season,week_num) as {col}'
              for col in rem_columns]


conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
cursor = conn.cursor()

def base_lead_table(year=datetime.now().year, week=None):
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
    df = pd.read_sql_query(query,conn)
    return df
        
def avg_season_stats(year, partition=0):
    if partition:
        partition_prefix = [f'''avg({col}) over (partition by team_id, season order by id ROWS BETWEEN {partition-1} PRECEDING AND 
            CURRENT ROW) as {col}_season_avg''' for col in columns if col not in grouped_cols]
        query = f'''
        select
        {', '.join(grouped_cols)}
        , {', '.join(partition_prefix)}
        from ncaaf_team_season_stats
        where season={year}
        and week_num > 1
        '''
        return pd.read_sql_query(query,conn).drop_duplicates()
    else:
        partition_prefix = [f'''avg({col}) over (partition by team_id, season order by id ROWS BETWEEN UNBOUNDED PRECEDING AND 
                    CURRENT ROW) as {col}_season_avg''' for col in columns if col not in grouped_cols]
        query = f'''
                select
                {', '.join(grouped_cols)}
                , {', '.join(partition_prefix)}
                from ncaaf_team_season_stats
                where season={year}
                and week_num > 1
                '''
        return pd.read_sql_query(query, conn).drop_duplicates()

def get_full_season_avgs_by_week(table):
    columns = pd.read_sql_query(f'select * from {table} where 1=0', conn).columns
    def set_prefix(prefix, columns):
        return [f'{prefix}.{col}' for col in columns]
    q_columns = [col for col in columns if col not in grouped_cols]
    query = f'''
    with last_week_of_season as (
        select 
        *,
        row_number() over (partition by season, team_id order by id desc) as last_week
        from {table}
    )   
    select * from (
     select 
     ss.team_team, 
     ss.team_id,
     ss.team_conference,
     ss.season, 
     ss.week_num, 
     ss.id,
     {', '.join(set_prefix('assbt',q_columns))}
     from ncaaf_team_season_stats ss
     join {table} assbt on assbt.id = ss.id and ss.team_id = assbt.team_id
 
    union all 

    select 
    ss.team_team, 
    ss.team_id,
    ss.team_conference,
    ss.season, 
    ss.week_num, 
    ss.id,
    {', '.join(set_prefix('lwos',q_columns))}
    from ncaaf_team_season_stats ss
    join last_week_of_season lwos on lwos.season = ss.season - 1 and lwos.team_id = ss.team_id and lwos.last_week = 1
    where ss.week_num = 1
    )
	order by team_id, season, id
    '''
    return pd.read_sql_query(query, conn)
    
    
    
    

    