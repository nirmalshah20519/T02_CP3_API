import pandas as pd
import pickle

Winscore = pd.read_csv('GroundWinScore.csv')

PointTable = pd.read_csv('FinalPointTable.csv')

Grounds = list(Winscore['Ground'])

Teams = list(PointTable['Team'])


def create_normal_input(team_1, team_2, ground):
  t1_winscore = Winscore.loc[Winscore['Ground'] == ground, team_1].values[0]
  t2_winscore = Winscore.loc[Winscore['Ground'] == ground, team_2].values[0]
  input_dict = {'Team_1':team_1, 'Team_2':team_2, 'Team_1_Winscore':t1_winscore, 'Team_2_Winscore':t2_winscore, 'winning_team':None}
  input_df = pd.DataFrame([input_dict])
  return input_df


def create_training_input(existing_df):
  teams = list(PointTable['Team'].unique())
  teams = sorted(teams)
  new_df = []
  for index, row in existing_df.iterrows():
    input_dict = {}
    for team in teams:
        input_dict[f'Team_1_{team}'] = 0
        input_dict[f'Team_2_{team}'] = 0
    t1 = row['Team_1']
    t2 = row['Team_2']
    input_dict[f'Team_1_{t1}'] = 1
    input_dict[f'Team_2_{t2}'] = 1

    input_dict['Team_1_Winscore'] = row['Team_1_Winscore']
    input_dict['Team_2_Winscore'] = row['Team_2_Winscore']
    
    new_df.append(input_dict)
  return pd.DataFrame(new_df)
