import os

import pandas as pd
import sklearn
from flask import jsonify
from flask_restful import Resource
from sklearn.cluster import KMeans

from .utils import DATA_ROOT, calculate_ratings, CLUSTERING_PRED
    
# testapi: http://127.0.0.1:8000/api/clustering_advanced_stat/10.0-10.0-10.0-10.0-10.0-10.5-1.0-1.0-1.0-1.0-1.0-1.0-1.0_10.0-10.0-10.0-10.0-10.0-10.5-1.0-1.0-1.0-1.0-1.0-1.0-1.0
class GetClusteringBoxscoreAdvancedStat(Resource):

    def get(
            self, 
            AST_home,
            BLK_home,
            DREB_home,
            FG3A_home,
            FG3M_home,
            FGA_home,
            FGM_home,
            FTA_home,
            FTM_home,
            OREB_home,
            PF_home,
            STL_home,
            TO_home,
            AST_away,
            BLK_away,
            DREB_away,
            FG3A_away,
            FG3M_away,
            FGA_away,
            FGM_away,
            FTA_away,
            FTM_away,
            OREB_away,
            PF_away,
            STL_away,
            TO_away
            ):
        
        # load precomputed boxscores of all teams
        df_boxscores = pd.read_csv(os.path.join(DATA_ROOT, 'precomputed', 'boxscores.csv'), index_col=0)

        # add custom boxscores
        df_custom = pd.DataFrame({
            'AST': [AST_home, AST_away],
            'BLK': [BLK_home, BLK_away],
            'DREB': [DREB_home, DREB_away],
            'FG3A': [FG3A_home, FG3A_away],
            'FG3M': [FG3M_home, FG3M_away],
            'FGA': [FGA_home, FGA_away],
            'FGM': [FGM_home, FGM_away],
            'FTA': [FTA_home, FTA_away],
            'FTM': [FTM_home, FTM_away],
            'OREB': [OREB_home, OREB_away],
            'PF': [PF_home, PF_away],
            'STL': [STL_home, STL_away],
            'TO': [TO_home, TO_away],
            'is_home': [True, False],
            'TEAM_ID': [1, 0],
        })

        # calculate clustering from boxscores of original teams (doesn't change)
        df_clustering = calculate_ratings(df_boxscores)

        # calculate clustering of custom teams
        df_custom_clustering = calculate_ratings(df_custom.copy())

        # combine clustering data from original teams and custom teams
        df_clustering = pd.concat([df_clustering, df_custom_clustering], axis=0)

        # fit the clustering model using ratings
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(df_clustering[CLUSTERING_PRED])
        df_clustering['cluster'] = kmeans.labels_

        return jsonify(df_clustering.to_dict("records"))