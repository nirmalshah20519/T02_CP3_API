from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import pickle

datafile = pd.read_csv('deliveries.csv')

Venues = list(datafile['venue'].unique())

with open('task1_run_pred.pkl', 'rb') as file:
    task_1_model = pickle.load(file)

def api_test(data_csv,venue='Narendra Modi Stadium, Ahmedabad',batting_team="India",bowling_team='South Africa',match_id='32',innings=1,ball=50.0,total_extras=16,total_wides=5,total_noballs=5,total_byes=4,total_legbyes=2):
    cd = [ 'season', 'start_date','other_wicket_type',
       'other_player_dismissed','penalty', 'player_dismissed',]
    filled = data_csv.drop(columns=cd)
    filled.isnull().sum()
    filled  = filled.fillna(0)
    filled.isnull().sum()

    filled['total_runs'] = filled.groupby(['match_id', 'innings'])['runs_off_bat'].cumsum() + filled.groupby(['match_id', 'innings'])['extras'].cumsum() + filled.groupby(['match_id', 'innings'])['wides'].cumsum() + filled.groupby(['match_id', 'innings'])['byes'].cumsum() + filled.groupby(['match_id', 'innings'])['legbyes'].cumsum()
    filled['total_runs_off_bat'] = filled.groupby(['match_id', 'innings'])['runs_off_bat'].cumsum()
    filled['total_extras'] = filled.groupby(['match_id', 'innings'])['extras'].cumsum()
    filled['total_wides'] = filled.groupby(['match_id', 'innings'])['wides'].cumsum()
    filled['total_noballs'] = filled.groupby(['match_id', 'innings'])['noballs'].cumsum()
    filled['total_byes'] = filled.groupby(['match_id', 'innings'])['byes'].cumsum()
    filled['total_legbyes'] = filled.groupby(['match_id', 'innings'])['legbyes'].cumsum()
    
    max_ball_indices = filled.groupby(['match_id', 'innings'])['ball'].idxmax()
    result_df = filled.loc[max_ball_indices, ['match_id', 'innings', 'venue', 'ball', 'batting_team', 'bowling_team',
                                         'total_runs', 'total_extras', 'total_wides', 'total_noballs',
                                       'total_byes', 'total_legbyes']].reset_index(drop=True)

    X = result_df.drop(columns='total_runs')
    Y = result_df['total_runs']

    X_e = pd.get_dummies(X, columns=[ 'match_id','innings','venue', 'batting_team', 'bowling_team',], prefix='Category')

    
    scaler = StandardScaler()
    X_es = scaler.fit_transform(X_e)

    data = {
    'match_id': [match_id],
    'innings': [innings],
    'ball': [ball],
    'venue': [venue],
    'batting_team': [batting_team],
    'bowling_team': [bowling_team],
    "total_extras": [total_extras],
    'total_wides': [total_wides],
    'total_noballs': [total_noballs],
    'total_byes': [total_byes],
    'total_legbyes': [total_legbyes],
    }

    df = pd.DataFrame(data)
    # print(df)
# Group by 'match_id' and 'innings' and calculate the sum of relevant columns within each group
    result = df.groupby(['match_id', 'innings', 'venue', 'ball', 'batting_team', 'bowling_team']).agg({
    'total_extras': 'sum',
    'total_wides': 'sum',
    'total_noballs':'sum',
    'total_byes': 'sum',
    'total_legbyes': 'sum'
    }).reset_index()

    result = pd.concat([result,X], axis=0)
    # print(result_df)
    Xt_e = pd.get_dummies(result, columns=[ 'match_id','innings','venue', 'batting_team', 'bowling_team',], prefix='Category')
    Xt_e = Xt_e.head(1)
    scaler = StandardScaler()
    X_es = scaler.fit_transform(Xt_e)
    # print(X_es[2:].shape)
    X_es = np.delete(X_es,0)
    X_es = X_es.reshape(1,70)
    return X_es 

