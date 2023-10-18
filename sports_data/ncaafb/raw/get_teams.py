import requests
import pandas as pd
from sports_data.ncaafb.utilities.constants import *
from datetime import datetime

def get_teams():
        df = pd.read_html(teams_url)[0]
        df.columns = df.columns.droplevel(level=0)
        return df[['School']].dropna()

def get_year():
    return datetime.now().year 

def format_teams():
    df = get_teams()
    df['Abbreviation'] = df.School.apply(lambda x: x.lower().replace(' ', '-'))
    return df
    