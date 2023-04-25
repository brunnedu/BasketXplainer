import os
import pickle

import lightgbm as lgb
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# global constants
DATA_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
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


def get_clustering(df_boxscores: pd.DataFrame, n_components: int = 2, n_clusters: int = 3):
    """
    Add clustering columns to boxscore dataframe
    """
    
    df_clustering = df_boxscores.copy()
    
    # standardize data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_clustering[PRED_COLS])
    
    # perform pca
    pca = PCA(n_components=n_components)
    pca_data = pca.fit_transform(scaled_data)
    
    # perform kmeans
    # kmeans = KMeans(n_clusters=n_clusters, n_init=10)
    # kmeans.fit(pca_data)
    
    # add clustering columns
    df_clustering['x_coord'] = [coord[0] for coord in pca_data]
    df_clustering['y_coord'] = [coord[1] for coord in pca_data]
    # df_cluster['cluster'] = kmeans.labels_
    
    return df_clustering, scaler, pca