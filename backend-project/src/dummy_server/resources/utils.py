import os
import pandas as pd
import lightgbm as lgb
import pickle

# global constants
DATA_ROOT = os.path.join(".", "data")
PRED_COLS = ['AST', 'BLK', 'DREB', 'FG3A', 'FG3M', 'FGA', 'FGM', 'FTA', 'FTM', 'OREB', 'PF', 'STL', 'TO']


def load_model(path_to_model_str: str = os.path.join(DATA_ROOT, 'precomputed', 'lightgbm.txt')):
    """
    Load stored LightGBM model
    """

    # read model string from disk
    with open(path_to_model_str, 'r') as f:
        model_str = f.read()

    # load lightgbm booster from model string
    model = lgb.Booster(model_str=model_str)

    return model


def load_tree_explainer(path_to_tree_explainer: str = os.path.join(DATA_ROOT, 'precomputed', 'TreeExplainer.pkl')):
    """
    Load stored SHAP TreeExplainer of the lightgbm model
    """

    with open(path_to_tree_explainer, 'rb') as f:
        explainer = pickle.load(f)

    return explainer


def get_team_boxscore(team_id=1610612738, is_home=True) -> pd.DataFrame:
    """
    Calculate aggregated team boxscores from raw datasets
    """

    games = pd.read_csv(os.path.join(DATA_ROOT, 'dataset_games.csv'))
    games_details = pd.read_csv(os.path.join(DATA_ROOT, 'dataset_games_details.csv'))

    # join games to games_details for date information
    games_details = games_details.merge(games, on='GAME_ID')

    # add additional column indicating whether team is home or not
    games_details['is_home'] = games_details['TEAM_ID'] == games_details['TEAM_ID_home']

    # select data from team at home or away
    games_details = games_details[(games_details['TEAM_ID']==team_id) & (games_details['is_home']==is_home)][PRED_COLS+['GAME_ID']]

    # sum over all players for each game and then average over all games
    boxscore = games_details.groupby(['GAME_ID']).sum().mean().to_frame().T
    
    return boxscore