import pandas as pd 
import datetime
import sqlite3
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

import requests

def get_espn_odds():
    url = 'https://www.espn.com/mens-college-basketball/lines'
    driver = webdriver.Chrome()
    driver.get(url)
    has_data = False
    tries = 0
    while not has_data:
        try:
            show_more = driver.find_element(By.CSS_SELECTOR,'a.AnchorLink.loadMore__link')
            show_more.click()
            time.sleep(10)
        except:
            has_data = True
    
    page = driver.page_source
    data = pd.read_html(page)
    driver.quit()
    # print(data)
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
    df['away_team'] = df['away_team'].apply(lambda x: re.sub(r'\d','',x))
    df['home_team'] = df['home_team'].apply(lambda x: re.sub(r'\d','',x))
    df['away_ml'] = df['away_ml'].apply(lambda i: str(i) if str(i) == '--' else int(i))
    df['home_ml'] = df['home_ml'].apply(lambda i: str(i) if str(i) == '--' else int(i))
    df['line_t'] = df.apply(lambda r: max(r.line, r.spread), axis=1)
    df['spread_t'] = df.apply(lambda r: min(r.line, r.spread), axis=1)
    df['line'] = df['line_t']
    df['spread'] = df['spread_t']
    f = df.drop(['line_t','spread_t'], axis=1)
    f['date_upd'] = datetime.datetime.now()
    return f
        
    