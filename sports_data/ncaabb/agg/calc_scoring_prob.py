import pandas as pd 
import datetime
import sqlite3

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
# cursor = conn.cursor()

raw = pd.read_json('https://barttorvik.com/trank.php?json=1')
raw = raw.drop([27,28,29,30,31,32,33],axis=1)
columns = ['team','adjoe','adjde','barthag','rec','g','u','efg','efgd','ftr','ftrd','tor','tord',
           'orb','drb','u1','2p%','2p%d','3p%','3p%d','d_block%','o_block%','AstR','dAstR',
           '3pR','d3pR','Adj_T', 'wab','ft%','dft%']
raw.columns = columns


ncaa_adj_t = sum(raw.Adj_T)/len(raw.Adj_T)
ncaa_efg = sum(raw.efg)/len(raw.efg)
ncaa_de = sum(raw.adjde)/len(raw.adjde)

def exp_fg_att(fga_a,tempo,adj_tempo):
    return fga_a * (exp_tempo(pos_adj_a, pos_adj_b) / adj_tempo)

def exp_tempo(pos_adj_a, pos_adj_b):
    return (pos_adj_a/ncaa_adj_t) * (pos_adj_b/ncaa_adj_t) * ncaa_adj_t

def exp_pos(efg_a, efgd_b):
    return (efg_a/ncaa_efg) * (efgd_b/ncaa_efg) * (efg_a/100)

def pred_points(oe_a,de_b, tempo):
    return (oe_a * de_b * tempo) / (ncaa_de * 100)

def points_variance(pos_adj_a, pos_adj_b):
    return exp_fg_att