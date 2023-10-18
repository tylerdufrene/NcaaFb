import pandas as pd 
import sqlite3
from datetime import datetime

conn = sqlite3.connect(r'C:\Users\Tyler Dufrene\Documents\TylerDufrene\Data Science\sports_data\ncaafb\sports_reference.db')
cursor = conn.cursor()

def format_game_stats(year=None, week=None):
    if week:
        results = pd.read_sql_query(
            f'''
            select * from ncaaf_game_stats
            where season = {year}
            and week_num = {week}
            ''', conn
        )
    elif year:
        results = pd.read_sql_query(
            f'''
            select * from ncaaf_game_stats
            where season = {year}
            ''', conn
        )
    else:
        results = pd.read_sql_query(
            f'''
            select * from ncaaf_game_stats
            ''', conn
        )
    results['home_total_penalties'] = results['home_totalPenaltiesYards'].apply(lambda x: str(x).split('-')[0])
    results['home_total_penalty_yards'] = results['home_totalPenaltiesYards'].apply(lambda x: str(x).split('-')[1] if str(x).__contains__('-') else 0)
    results['home_yards_per_penalty'] = results['home_total_penalty_yards'].astype(int) / results['home_total_penalties'].astype(int)
    results['home_thirdDownEff'] = results['home_thirdDownEff'].apply(lambda x: '0-0' if not str(x).__contains__('-') else str(x))
    results['home_thirdDownEff'] = results['home_thirdDownEff'].apply(lambda x: int(str(x).split('-')[0])/int(str(x).split('-')[1])
                                                                        if int(str(x).split('-')[1]) > 0 else 0)
    results['home_possessionTime'] = results['home_possessionTime'].apply(lambda x: str(x).replace(':','.'))
    results['home_fourthDownEff'] = results['home_fourthDownEff'].apply(lambda x: '0-0' if not str(x).__contains__('-') else str(x))
    results['home_fourthDownEff'] = results['home_fourthDownEff'].apply(lambda x: int(str(x).split('-')[0])/int(str(x).split('-')[1])
                                                                        if (str(x).split('-')[1].isnumeric() and int(str(x).split('-')[1])) > 0 else 0)
    results['home_completions'] = results['home_completionAttempts'].apply(lambda x: str(x).split('-')[0])
    results['home_completions_attempted'] = results['home_completionAttempts'].apply(lambda x: '0' if not str(x).__contains__('-') else str(x).split('-')[1])
    results['home_completion_percent'] = results['home_completions'].astype(int) / results['home_completions_attempted'].astype(int)
    ## Away Transforms
    results['away_total_penalties'] = results['away_totalPenaltiesYards'].apply(lambda x: str(x).split('-')[0])
    results['away_total_penalty_yards'] = results['away_totalPenaltiesYards'].apply(lambda x: str(x).split('-')[1] if str(x).__contains__('-') else 0)
    results['away_yards_per_penalty'] = results['away_total_penalty_yards'].astype(int) / results['away_total_penalties'].astype(int)
    results['away_thirdDownEff'] = results['away_thirdDownEff'].apply(lambda x: '0-0' if not str(x).__contains__('-') else str(x))
    results['away_thirdDownEff'] = results['away_thirdDownEff'].apply(lambda x: int(str(x).split('-')[0])/int(str(x).split('-')[1])
                                                                        if (str(x).split('-')[1].isnumeric() and  int(str(x).split('-')[1]) > 0) else 0)
    results['away_possessionTime'] = results['away_possessionTime'].apply(lambda x: str(x).replace(':','.'))
    results['away_fourthDownEff'] = results['away_fourthDownEff'].apply(lambda x: '0-0' if not str(x).__contains__('-') else str(x))
    results['away_fourthDownEff'] = results['away_fourthDownEff'].apply(lambda x: int(str(x).split('-')[0])/int(str(x).split('-')[1])
                                                                        if (str(x).split('-')[1].isnumeric() and  int(str(x).split('-')[1]) > 0) else 0)
    results['away_possessionTime'] = results['away_possessionTime'].apply(lambda x: str(x).replace(':','.'))
    results['away_completions'] = results['away_completionAttempts'].apply(lambda x: str(x).split('-')[0])
    results['away_completions_attempted'] = results['away_completionAttempts'].apply(lambda x: '0' if not str(x).__contains__('-') else str(x).split('-')[1])
    results['away_completion_percent'] = results['away_completions'].astype(int) / results['away_completions_attempted'].astype(int)
    return results.drop_duplicates()
    