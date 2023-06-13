import os

import pandas as pd
import numpy as np
from flask import jsonify
from flask_restful import Resource
from sklearn.cluster import KMeans

from .utils import DATA_ROOT, calculate_ratings, calculate_custom_ratings, CLUSTERING_PRED, load_new_stat_classifier, PRED_COLS
    
# testapi: http://127.0.0.1:8000/api/clustering_advanced_stat/10.0-10.0-10.0-10.0-10.0-10.5-1.0-1.0-1.0-1.0-1.0-1.0-1.0_10.0-10.0-10.0-10.0-10.0-10.5-1.0-1.0-1.0-1.0-1.0-1.0-1.0
class GetClusteringBoxscoreAdvancedStat(Resource):

    def get(
            self, 
            AST_home,
            BLK_home,
            DREB_home,
            FG3A_home,
            FGA_home,
            FTA_home,
            OREB_home,
            STL_home,
            TO_home,
            AST_away,
            BLK_away,
            DREB_away,
            FG3A_away,
            FGA_away,
            FTA_away,
            OREB_away,
            STL_away,
            TO_away
            ):
        
        # load precomputed boxscores of all teams
        df_boxscores = pd.read_csv(os.path.join(DATA_ROOT, 'precomputed', 'boxscores.csv'), index_col=0)

        # calculate clustering from boxscores of original teams (doesn't change)
        df_clustering = calculate_ratings(df_boxscores)

        # add custom boxscores
        df_custom = pd.DataFrame({
            'AST': [AST_home, AST_away],
            'BLK': [BLK_home, BLK_away],
            'DREB': [DREB_home, DREB_away],
            'FG3A': [FG3A_home, FG3A_away],
            'FG3M': [-1, -1],
            'FGA': [FGA_home, FGA_away],
            'FGM': [-1, -1],
            'FTA': [FTA_home, FTA_away],
            'FTM': [-1, -1],
            'OREB': [OREB_home, OREB_away],
            'PF': [-1, -1],
            'STL': [STL_home, STL_away],
            'TO': [TO_home, TO_away],
            'is_home': [True, False],
            'TEAM_ID': [1, 0],
        })

        # calculate clustering of custom teams
        df_custom_clustering = calculate_custom_ratings(df_custom.copy(), df_clustering.copy())

        # combine clustering data from original teams and custom teams
        df_clustering = pd.concat([df_clustering, df_custom_clustering], axis=0)

        # fit the clustering model using ratings
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(df_clustering[CLUSTERING_PRED])
        df_clustering['cluster'] = kmeans.labels_

        return jsonify(df_clustering.to_dict("records"))
    
class CalculateWiningOverview(Resource):
        def get(self, 
            AST_home,
            BLK_home,
            DREB_home,
            FG3A_home,
            FGA_home,
            FTA_home,
            OREB_home,
            STL_home,
            TO_home,
            AST_away,
            BLK_away,
            DREB_away,
            FG3A_away,
            FGA_away,
            FTA_away,
            OREB_away,
            STL_away,
            TO_away):

            predictions = {}

            df_boxscores = pd.read_csv(os.path.join(DATA_ROOT, 'precomputed', 'boxscores.csv'), index_col=0)

            model = load_new_stat_classifier()

            for index, row in df_boxscores.iterrows():
                home_inference = np.array([
                    AST_home, 
                    BLK_home,
                    DREB_home,
                    FG3A_home,
                    FGA_home,
                    FTA_home, 
                    OREB_home, 
                    STL_home,
                    TO_home, 
                    row["AST"], 
                    row["BLK"], 
                    row["DREB"],
                    row["FG3A"],
                    row["FGA"],
                    row["FTA"],
                    row["OREB"], 
                    row["STL"], 
                    row["TO"]
                ]).reshape(1, -1)

                away_inference = np.array([
                    AST_away, 
                    BLK_away,
                    DREB_away,
                    FG3A_away,
                    FGA_away,
                    FTA_away, 
                    OREB_away, 
                    STL_away,
                    TO_away, 
                    row["AST"], 
                    row["BLK"], 
                    row["DREB"],
                    row["FG3A"],
                    row["FGA"],
                    row["FTA"],
                    row["OREB"], 
                    row["STL"], 
                    row["TO"]
                ]).reshape(1, -1)

                home_proba = model.predict(home_inference)[0]
                away_proba = model.predict(away_inference)[0]
                predictions[row["TEAM_ID"]] = {'winning_odds_home': home_proba, "winning_odds_away": away_proba}

            return jsonify(predictions)