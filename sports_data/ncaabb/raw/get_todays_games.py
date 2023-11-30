import pandas as pd 
import datetime
import sqlite3

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\sports_reference.db')
# cursor = conn.cursor()


ratings = pd.read_json("https://barttorvik.com/2024_team_results.json")
ratings.columns = ["rank","TEAM","conf","record","ADJOE","oe Rank","ADJDE",
            "de Rank","BARTHAG",	"Bartrank",	"proj. W",	"Proj. L",	"Pro Con W",
            "Pro Con L",	"Con Rec.",	"sos",	"ncsos",	"consos",	"Proj. SOS",
            "Proj. Noncon SOS",	"Proj. Con SOS",	"elite SOS",	"elite noncon SOS",
            "Opp OE",	"Opp DE",	"Opp Proj. OE",	"Opp Proj DE",	"Con Adj OE",	"Con Adj DE",
            "Qual O",	"Qual D",	"Qual Barthag",	"Qual Games",	"FUN",	"ConPF",	"ConPA",
            "ConPoss",	"ConOE",	"ConDE",	"ConSOSRemain",	"Conf Win%",	"WAB",
            "WAB Rk",	"Fun Rk", "ADJ_T"]
ratings.to_sql('ncaab_toRvik_ratings',conn,if_exists='replace',index=False)

today = pd.read_csv('https://barttorvik.com/2024_master_sked.csv',header=None)
games_columns = ['id','date','empty1','empty2','away','home']
today.columns = games_columns
# Create a datetime object
now = datetime.datetime.now()
# Get the day
day = now.day
# Format the day with leading zero if less than 10
formatted_day = str(day).zfill(1)
today = today[today['date']==datetime.datetime.today().strftime(f"%m/{formatted_day}/%Y")]

x = today.merge(ratings,left_on='home',right_on='TEAM',suffixes=('_','_home')
                 ).merge(ratings,left_on='away',right_on='TEAM',suffixes=('_home','_away'))

x = x[['id', 'date', 'empty1', 'empty2', 'away', 'home', 'rank_home',
       'TEAM_home', 'conf_home', 'record_home', 'ADJOE_home', 'oe Rank_home',
       'ADJDE_home', 'de Rank_home', 'BARTHAG_home', 'Bartrank_home',
       'proj. W_home', 'Proj. L_home', 'Pro Con W_home', 'Pro Con L_home',
       'Con Rec._home', 'sos_home', 'ncsos_home', 'consos_home',
       'Proj. SOS_home', 'Proj. Noncon SOS_home', 'Proj. Con SOS_home',
       'elite SOS_home', 'elite noncon SOS_home', 'Opp OE_home', 'Opp DE_home',
       'Opp Proj. OE_home', 'Opp Proj DE_home', 'Con Adj OE_home',
       'Con Adj DE_home', 'Qual O_home', 'Qual D_home', 'Qual Barthag_home',
       'Qual Games_home', 'FUN_home', 'ConPF_home', 'ConPA_home',
       'ConPoss_home', 'ConOE_home', 'ConDE_home', 'ConSOSRemain_home',
       'Conf Win%_home', 'WAB_home', 'WAB Rk_home', 'Fun Rk_home',
       'ADJ_T_home', 'rank_away', 'TEAM_away', 'conf_away', 'record_away',
       'ADJOE_away', 'oe Rank_away', 'ADJDE_away', 'de Rank_away',
       'BARTHAG_away', 'Bartrank_away', 'proj. W_away', 'Proj. L_away',
       'Pro Con W_away', 'Pro Con L_away', 'Con Rec._away', 'sos_away',
       'ncsos_away', 'consos_away', 'Proj. SOS_away', 'Proj. Noncon SOS_away',
       'Proj. Con SOS_away', 'elite SOS_away', 'elite noncon SOS_away',
       'Opp OE_away', 'Opp DE_away', 'Opp Proj. OE_away', 'Opp Proj DE_away',
       'Con Adj OE_away', 'Con Adj DE_away', 'Qual O_away', 'Qual D_away',
       'Qual Barthag_away', 'Qual Games_away', 'FUN_away', 'ConPF_away',
       'ConPA_away', 'ConPoss_away', 'ConOE_away', 'ConDE_away',
       'ConSOSRemain_away', 'Conf Win%_away', 'WAB_away', 'WAB Rk_away',
       'Fun Rk_away', 'ADJ_T_away']]

adj_oe_ncaa = sum(ratings.ADJOE)/len(ratings.ADJOE)
adj_de_ncaa = sum(ratings.ADJDE)/len(ratings.ADJDE)
adjt_ncaa = sum(ratings.ADJ_T)/len(ratings.ADJ_T)

def win_ratio(adj_de, adj_oe):
    return 1/(1 + (adj_de/adj_oe)**11.5)

# Chance of Team a beating team b
def log5(pa,pb):
    return (pa - (pa*pb)) / ((pa + pb) - (2*pa*pb))

# Get the expected tempo of the two teams
def exp_tempo(adj_ta, adj_tb):
    return ((adj_ta/adjt_ncaa)*(adj_tb/adjt_ncaa))*adjt_ncaa

def get_team_score(adj_oe, adj_de, adj_ta, adj_tb, loc):
    et = exp_tempo(adj_ta, adj_tb)
    if loc == 'home':
        return (adj_oe*1.014)*((adj_de*1.014)/adj_de_ncaa)*(et/100)
    else:
        return (adj_oe*0.986)*((adj_de*0.986)/adj_de_ncaa)*(et/100)

def get_game_score(adj_oe_home, adj_de_home, adj_oe_away, adj_de_away, adj_t_home, adj_t_away):
    away_team = get_team_score(adj_oe_away, adj_de_home, adj_t_home, adj_t_away, 'away')
    home_team = get_team_score(adj_oe_home, adj_oe_away, adj_t_home, adj_t_away, 'home')
    return (home_team, away_team)

def get_todays_preds():
    raw = pd.read_json('https://barttorvik.com/2024_super_sked.json')
    columns = ['muid', 'date', 'conmatch', 'matchup', 'prediction', 'ttq', 'conf', 'venue',
            'team1', 't1oe', 't1de', 't1py', 't1wp', 't1propt', 'team2', 't2oe', 't2de', 't2py', 't2wp',
            't2propt', 'tpro', 't1qual', 't2qual', 'gp', 'result', 'tempo', 'possessions', 't1pts',
            't2pts', 'winner', 'loser', 't1adjt', 't2adjt', 't1adjo', 't1adjd', 't2adjo', 't2adjd',
            'gamevalue', 'mismatch', 'blowout', 't1elite', 't2elite', 'ord_date', 't1ppp', 't2ppp', 'gameppp',
            't1rk', 't2rk', 't1gs', 't2gs', 'gamestats', 'overtimes', 't1fun', 't2fun', 'results']
    raw.columns = columns
    raw['date'] = pd.to_datetime(raw['date'])
    today = raw[raw['date']==datetime.date.today().strftime('%Y-%m-%d')]
    df =  today[['team2','team1','t2wp','t2propt','t1propt']]
    df.columns = ['home','away','home_win_prob','game_score_home','game_score_away']
    df['spread'] = df['game_score_home'] - df['game_score_away']
    df['game_score_total'] = df['game_score_home'] + df['game_score_away']
    df['game_date'] = datetime.date.today()
    df['date_upd'] = datetime.datetime.now()
    df['source'] = 'auto'
    return df
    
def final_df(df):
    df['home_win_ratio'] = df.apply(lambda x: win_ratio(x.ADJDE_home, x.ADJOE_home), axis=1)
    df['away_win_ratio'] = df.apply(lambda x: win_ratio(x.ADJDE_away, x.ADJOE_away), axis=1)
    df['home_win_prob'] = df.apply(lambda x: log5(x.home_win_ratio, x.away_win_ratio), axis=1)
    df['game_score_home'] = df.apply(lambda x: get_team_score(x.ADJOE_home, x.ADJDE_away
                                                              , x.ADJ_T_home, x.ADJ_T_away, 'home'), axis=1)
    df['game_score_away'] = df.apply(lambda x: get_team_score(x.ADJOE_away, x.ADJDE_home
                                                              , x.ADJ_T_away, x.ADJ_T_home, 'away'), axis=1)
    df['spread'] = df.apply(lambda x: x.game_score_home - x.game_score_away, axis=1)
    df['game_score_total'] = df.apply(lambda x: x.game_score_home + x.game_score_away, axis=1)
    df['game_date'] = datetime.date.today()
    df['date_upd'] = datetime.datetime.now()
    df['source'] = 'manual'
    return df[['home', 'away','home_win_prob','game_score_home','game_score_away','spread', 
               'game_score_total','game_date','date_upd','source']]
    
def final_to_db():
    fdf = get_todays_preds()
    f = final_df(x)
    fdf.to_sql('ncaab_todays_game_predictions', conn, if_exists = 'replace', index=False)
    fdf.to_sql('ncaab_historic_game_predictions', conn, if_exists='append', index=False)
    f.to_sql('ncaab_historic_game_predictions',conn,if_exists='append', index=False)
    
if __name__ == '__main__':
    final_to_db()