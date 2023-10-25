import pandas as pd 

def get_teams():
    df = pd.read_html('https://www.sports-reference.com/cbb/schools/')[0]
    df = df[df['School']!='School']
    df = df.rename(columns={'To':'Last'})
    df['TeamLookup'] = df.School.apply(
        lambda s: str(s).lower().replace(' ','-').replace('(','').replace(')','').replace('&',''))
    df['Active'] = df.Last.apply(lambda x: int(x) >= 2020)
    return df[df['Active']==True]