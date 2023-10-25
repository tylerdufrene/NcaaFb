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
    df['favorite'] = df.apply(lambda s: s.home_team if int(s.spread) < 0 
                          else s.away_team if int(s.spread) > 0 else 'Unknown', axis=1)
    df['favorite_cover_spread'] = df.apply(lambda t: 1 if t.favorite == t.winner and abs(t.spread) <= abs(t.home_points - t.away_points) else 0,axis=1)
    df['total_cover'] = df.apply(lambda t: 1 if int(t.home_points) + int(t.away_points) >= int(t.over_under) else 0, axis=1)
    df['favorite_won'] = df.apply(lambda w: 1 if w.winner == w.favorite else 0, axis=1)
    return df 

def add_column(df, fn, column_name):
    df[column_name] = df.apply(fn,axis=1)
    return df

def agg_outcome(df, agg_column, fn=None):
    df = format_df(df)
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
        bin_edges = np.linspace(agg[agg_column].min(), agg[agg_column].max(), bin_count +1)
        agg['bin'] = pd.cut(agg[agg_column], bins=bin_edges)
        agg = agg.groupby('bin')[['id','total_cover','favorite_cover_spread','favorite_won']].sum().reset_index()
    agg['cover_p'] = agg.total_cover / agg.id 
    agg['fcs_p'] = agg.favorite_cover_spread / agg.id 
    agg['favorite_won_p'] = agg.favorite_won / agg.id
    return agg