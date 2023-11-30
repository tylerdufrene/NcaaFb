import pandas as pd 
import sqlite3
from datetime import datetime
import numpy as np
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
cursor = conn.cursor()

with open('historical_stats.sql', 'r') as sql_file:
    sql_query = sql_file.read()
    
df = pd.read_sql_query(sql_query, conn)

def format_df(df):
    df = df[~df['spread'].isna()]
    df['favorite'] = df.apply(lambda s: s.home_team if int(s.spread) < 0 
                          else s.away_team if int(s.spread) > 0 else 'Unknown', axis=1)
    df['underdog'] = df.apply(lambda t: t.home_team if t.favorite == t.away_team else t.away_team, axis=1)
    df['hm_team'] = df.apply(lambda t: 'favorite' if t.favorite == t.home_team else 'underdog',axis=1)
    try:
        df['favorite_cover_spread'] = df.apply(lambda t: 1 if t.favorite == t.winner and abs(t.spread) <= abs(t.home_points - t.away_points) else 0,axis=1)
        df['total_cover'] = df.apply(lambda t: 1 if int(t.home_points) + int(t.away_points) >= int(t.over_under) else 0, axis=1)
        df['favorite_won'] = df.apply(lambda w: 1 if w.winner == w.favorite else 0, axis=1)
    except:
        pass
    return df 

def get_favorite_stats(df):
    favorites_home = df[df['favorite']==df['home_team']]
    favorites_away = df[df['favorite']==df['away_team']]
    fcols = [col_name.replace('home','favorite') if col_name.__contains__('home') else col_name for col_name in df.columns]
    fcols2 = [col_name.replace('away','underdog') if col_name.__contains__('away') else col_name for col_name in fcols]
    sorted(fcols2)
    favorites_home.columns = fcols2 
    
    fa_cols = [col_name.replace('home','underdog') if col_name.__contains__('home') else col_name for col_name in df.columns]
    fa_cols2 = [col_name.replace('away','favorite') if col_name.__contains__('away') else col_name for col_name in fa_cols]
    sorted(fa_cols2)
    favorites_away.columns = fa_cols2
    return pd.concat([favorites_home,favorites_away])
        

def add_column(df, fn, column_name):
    df[column_name] = df.apply(fn,axis=1)
    return df

def agg_outcome(df, agg_column, fn=None):
    df = get_favorite_stats(format_df(df))
    if fn is not None:
        df = add_column(df, fn, agg_column)
        agg =  df.groupby(agg_column).agg({
        'id':'count',
        'total_cover':'sum',
        'favorite_cover_spread':'sum',
        'favorite_won':'sum'
        }).reset_index()
    else:
        agg = df.groupby(agg_column).agg({
        'id':'count',
        'total_cover':'sum',
        'favorite_cover_spread':'sum',
        'favorite_won':'sum'
        }).reset_index()
    if (agg[agg_column].dtype == 'float') | (agg[agg_column].dtype == 'int'):
        bin_count = 20
        # bin_edges = np.linspace(agg[agg_column].min(), agg[agg_column].max(), bin_count +1)
        agg['bin'] = pd.qcut(agg[agg_column], q=bin_count)
        agg = agg.groupby('bin')[['id','total_cover','favorite_cover_spread','favorite_won']].sum().reset_index()
    agg['cover_p'] = agg.total_cover / agg.id 
    agg['fcs_p'] = agg.favorite_cover_spread / agg.id 
    agg['favorite_won_p'] = agg.favorite_won / agg.id
    return agg

def current_betting_trends(df):
    spread = agg_outcome(df, 'spread_outcome',lambda x: ((1.1*(0.1 + x.favorite_avg_points - x.favorite_opp_points) / x.favorite_sos)) - ((0.1 + x.underdog_avg_points - x.underdog_opp_points) / x.underdog_sos) if x.hm_team =='favorite' else
                (((0.1 + x.favorite_avg_points - x.favorite_opp_points) / x.favorite_sos)) - (((0.1 + x.underdog_avg_points - x.underdog_opp_points) / x.underdog_sos)*1.1)
                )
    over_under = agg_outcome(df, 'ou_prob',lambda x: (((((x.favorite_avg_points + x.favorite_opp_points)/(x.favorite_sos * (1/x.underdog_sos))) + ((x.underdog_avg_points + x.underdog_opp_points))/x.underdog_sos * (1/x.favorite_sos)))/2) - x.over_under)
    spread['lower'] = spread.bin.apply(lambda a: a.left)
    spread['upper'] = spread.bin.apply(lambda a: a.right)
    over_under['lower'] = over_under.bin.apply(lambda a: a.left)
    over_under['upper'] = over_under.bin.apply(lambda a: a.right)
    spread_f = spread[['id', 'total_cover', 'favorite_cover_spread', 'favorite_won',
       'cover_p', 'fcs_p', 'favorite_won_p', 'lower', 'upper']]
    ou_f = over_under[['id', 'total_cover', 'favorite_cover_spread', 'favorite_won',
       'cover_p', 'fcs_p', 'favorite_won_p', 'lower', 'upper']]
    spread_f.to_sql('ncaaf_odds_static',conn, if_exists='replace', index=False)
    ou_f.to_sql('ncaaf_odds_static_over_under',conn, if_exists='replace', index=False)


current_betting_trends(df)