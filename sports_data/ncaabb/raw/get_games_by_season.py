import pandas as pd 
import datetime
import sqlite3

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
# cursor = conn.cursor()

columns = ['muid','date','conferences','matchup','prediction','ttq','conf','venue','team1',
           't1_off_eff','t1_def_eff','t1py','t1wp','t1propt','team2','t2_off_eff',
           't2_def_eff','t2py','t2wp','t2propt','tpro','t1qual','t2qual','gp','result']

today = pd.read_csv('https://barttorvik.com/2024_super_sked.csv',header=None)