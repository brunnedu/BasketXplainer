from flask_restful import Resource
from flask import jsonify, request
import pandas as pd
import numpy as np

STATISTICS = ["2FG%", "3FG%", "Assists", "Rebounds"]

class GetSHAPValuesTeam(Resource):
    """Get the prediction btw two teams"""

    #TODO: THiS IS A PLACEHOLDER!!! Need to cahnge it later
    def get(self, team_id_home, team_id_away):
        """Get the winning odds for two teams."""
        prediction = {}
        for stat in STATISTICS:
            prediction[stat] = 2
        prediction["Average_score"] = 100
        prediction["Difference"] = 8
        return jsonify(prediction)
    

class GetSHAPValuesBoxscore(Resource):

    def get(
            self, 
            FGM_home, 
            FGA_home, 
            FG3M_home, 
            FG3A_home, 
            FTM_home, 
            FTA_home, 
            OREB_home, 
            DREB_home, 
            AST_home, 
            STL_home, 
            BLK_home, 
            TO_home, 
            PF_home, 
            FGM_away, 
            FGA_away, 
            FG3M_away, 
            FG3A_away, 
            FTM_away, 
            FTA_away, 
            OREB_away, 
            DREB_away, 
            AST_away, 
            STL_away, 
            BLK_away, 
            TO_away, 
            PF_away
            ):
        """Get the SHAP feature importance values based on the boxscore stats"""

        data_dict = {
            'FGM_home': [FGM_home], 
            'FGA_home': [FGA_home], 
            'FG3M_home': [FG3M_home], 
            'FG3A_home': [FG3A_home], 
            'FTM_home': [FTM_home], 
            'FTA_home': [FTA_home], 
            'OREB_home': [OREB_home], 
            'DREB_home': [DREB_home], 
            'AST_home': [AST_home], 
            'STL_home': [STL_home], 
            'BLK_home': [BLK_home], 
            'TO_home': [TO_home], 
            'PF_home': [PF_home], 
            'FGM_away': [FGM_away], 
            'FGA_away': [FGA_away], 
            'FG3M_away': [FG3M_away], 
            'FG3A_away': [FG3A_away], 
            'FTM_away': [FTM_away], 
            'FTA_away': [FTA_away], 
            'OREB_away': [OREB_away], 
            'DREB_away': [DREB_away], 
            'AST_away': [AST_away], 
            'STL_away': [STL_away], 
            'BLK_away': [BLK_away], 
            'TO_away': [TO_away], 
            'PF_away': [PF_away]
        }

        df_X = pd.DataFrame(data_dict)

        # TODO: implement SHAP value calculation

        # dummy SHAP values
        prediction = {
            feat: np.random.rand() for feat in data_dict
        }
        
        return jsonify(prediction)