import pandas as pd 
import sqlite3
from datetime import datetime
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)


from raw.get_teams2 import get_all_teams
from raw.get_season_schedule import get_calendar
from raw.get_games import get_game_schedule
from raw.get_game_stats import get_game_stats
from agg.format_game_stats import format_game_stats
from agg.season_summary import get_home_and_away_stats
from agg.season_summary_agg import base_lead_table, avg_season_stats, get_full_season_avgs_by_week

format_game_stats = format_game_stats


conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
cursor = conn.cursor()

def query_db(table,year=None,week=None):
    if week:
        df = pd.read_sql_query(
            f'''
            select * from {table}
            where season={year}
            and week_num={week}
            ''', conn
        )
    elif year:
            df = pd.read_sql_query(
            f'''
            select * from {table}
            where season={year}
            ''', conn
        )
    else:
            df = pd.read_sql_query(
            f'''
            select * from {table}
            ''', conn
        )
    return df

def delete_statement(table, year=None, week=None):
    if week:
        return f'''
            DELETE FROM {table}
            where season = {year}
            and week_num={week}
            '''
    elif year:
                return f'''
            DELETE FROM {table}
            where season = {year}
            '''
    else:
        return f'''
                DROP TABLE IF EXISTS {table}
                '''

def all_teams_to_db():
    if data_exists('ncaaf_all_teams'):
        cursor.execute(delete_statement('ncaaf_all_teams'))
    get_all_teams().to_sql('ncaaf_all_teams', if_exists='replace',index=False, con=conn)
    

def data_exists(table, year=None, week=None):
    table_exists = False
    try:
        if week:
            q = pd.read_sql_query(f'select * from {table} where season={year} and week_num={week} limit 10', conn)
        else:
            q = pd.read_sql_query(f'select * from {table} where season={year} limit 10',conn)
        if len(q) > 1:
            table_exists = True 
    except:
        pass
    return table_exists 

        
def calendar_2_db(year=datetime.now().year):
    if data_exists('ncaaf_season_calendar',year):
        cursor.execute(delete_statement('ncaaf_season_calendar',year))
    get_calendar(year).to_sql('ncaaf_season_calendar', if_exists='append',index=False, con=conn)
    
def game_schedule_2_db(year=datetime.now().year, week=None):
    if data_exists('ncaaf_game_schedule',year,week):
        cursor.execute(delete_statement('ncaaf_game_schedule',year,week))
    get_game_schedule(year,week).to_sql('ncaaf_game_schedule',if_exists='append',index=False,con=conn)
    
 
def general_stats_2_db(fn, table,year=datetime.now().year, week=None, partition=0):
    if data_exists(table,year,week):
        cursor.execute(delete_statement(table,year,week))
    fn(year,week).to_sql(table,if_exists='append',index=False,con=conn)
    
    
def run_db(fn, table, year=None, week=None):
    if week:
        week_years = pd.read_sql_query(f'''
                                       select distinct week, year from ncaaf_season_calendar
                                       where year = {year}
                                       and week = {week}
                                       ''',conn)
    elif year:
        week_years = pd.read_sql_query(f'''
                                       select distinct week, year from ncaaf_season_calendar
                                       where year = {year}
                                       ''',conn)
    else:
        week_years = pd.read_sql_query(f'''
                                       select distinct week, year from ncaaf_season_calendar
                                       ''',conn)
    week_tuple = [(row.week, row.year) for row in week_years.itertuples(index=False)]
    for wk in week_tuple:
        if not wk[0]:
            pass
        if wk[0] > 16:
            pass 
        else:
            general_stats_2_db(fn, table, year=wk[1],week=wk[0])
            
## Materializing the lower level functions

    
# First year for this data is 2004
def game_stats_2_db(year, week=None):
    run_db(get_game_stats, 'ncaaf_game_stats',year,week)

def format_game_stats_2_db(year,week=None):
    run_db(format_game_stats,'ncaaf_game_stats_formatted', year, week)

def team_game_stats_2_db(year, week=None):
    run_db(get_home_and_away_stats, 'ncaaf_game_stats_by_team', year,week)

def team_season_summary_2_db(year):
    general_stats_2_db(base_lead_table,'ncaaf_team_season_stats', year)

def avg_season_summary_2_db(year, partition=None):
    general_stats_2_db(avg_season_stats,'ncaaf_avg_season_stats_by_team', year,partition=partition)

def avg_last_3_games_2_db(year, partition=4):
    general_stats_2_db(avg_season_stats, 'ncaaf_avg3_season_stats_by_team', year, partition=partition)

def avg_last_5_games_2_db(year, partition=6):
    general_stats_2_db(avg_season_stats, 'ncaaf_avg5_season_stats_by_team', year, partition=partition)

def avg_full_season_total(table):
    get_full_season_avgs_by_week(table).to_sql(table+'_total',if_exists='append',index=False,con=conn)

def create_game_summary_table():
    cursor.execute('DROP TABLE IF EXISTS ncaaf_game_summary;')
    cursor.execute(
        '''
        CREATE TABLE ncaaf_game_summary as
        select gs.*
            , gst.home_points
            , gst.away_points
            , case when gst.home_points > gst.away_points then gs.home_team else gs.away_team end as winner
            from ncaaf_game_schedule gs 
            join ncaaf_game_stats gst on gst.id = gs.id
        '''
    )