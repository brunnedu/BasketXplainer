import os

import pandas as pd
import sklearn
from flask import jsonify
from flask_restful import Resource
from sklearn.cluster import KMeans

from .utils import DATA_ROOT, PRED_COLS, calculate_ratings, get_clustering, CLUSTERING_PRED


class GetClusteringTeam(Resource):

    def get(self):
        # TODO: implement clustering model and replace dummy data with real data

        # hardcode dummy data
        dummy_data = pd.DataFrame({
            'team_id': [1610612738, 1610612744, 1610612748, 1610612742, 1610612756, 1610612749, 1610612755, 1610612763, 1610612750, 1610612761, 1610612740, 1610612762, 1610612751, 1610612741, 1610612743, 1610612737, 1610612739, 1610612746, 1610612766, 1610612745, 1610612752, 1610612753, 1610612757, 1610612759, 1610612765, 1610612764, 1610612747, 1610612754, 1610612760, 1610612758],
            'x_coord': [0.01, 0.84, 0.97, 0.43, 0.33, 0.76, 0.96, 0.39, 0.7, 0.82, 0.38, 0.62, 0.62, 0.58, 0.33, 0.21, 0.49, 0.39, 0.62, 0.08, 0.74, 0.96, 0.68, 0.37, 0.72, 0.12, 0.98, 0.01, 0.83, 0.23],
            'y_coord': [0.21, 0.12, 0.16, 0.15, 0.73, 0.12, 0.07, 0.28, 0.12, 0.85, 0.48, 0.95, 0.48, 0.66, 0.89, 0.16, 0.97, 0.29, 0.47, 0.21, 0.14, 0.76, 0.36, 0.97, 0.15, 0.48, 0.53, 0.24, 0.23, 0.56],
            'cluster_index': [1, 0, 2, 1, 0, 2, 2, 2, 2, 1, 1, 1, 3, 2, 2, 3, 2, 0, 0, 3, 2, 1, 0, 0, 3, 3, 0, 1, 0, 0],
            'hover_details': ['b21','vff','y4p','osz','qe3','xpo','fck','pzj','opq','sd8','ykz','tmi','dve','n0l','dnc','uoe','21j','vvt','9gv','yp0','c6j','h18','1jm','e6s','vxv','id0','sgn','5fs', '3la', 'ak4'],
        })

        data = dummy_data

        return jsonify(data.to_dict("records"))
    
# testapi: http://127.0.0.1:8000/api/clustering/10.0-10.0-10.0-10.0-10.0-10.5-1.0-1.0-1.0-1.0-1.0-1.0-1.0_10.0-10.0-10.0-10.0-10.0-10.5-1.0-1.0-1.0-1.0-1.0-1.0-1.0
class GetClusteringBoxscore(Resource):

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