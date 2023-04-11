from flask_restful import Resource
from flask import jsonify
import numpy as np
from .utils import load_model, PRED_COLS

class GetPredictionTeam(Resource):
    """Get the prediction btw two teams"""

    #TODO: THiS IS A PLACEHOLDER!!! Need to cahnge it later
    def get(self, team_id_home, team_id_away):
        """Get the winning odds for two teams."""
        
        return jsonify({'winning_odds_home': 0.37})
    

class GetPredictionBoxscore(Resource):

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
        """Get the predicted winning odds of the home team based on the boxscore stats"""

        # TODO: load model and perform inference

        X_inference = np.array([
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
        ]).reshape(1, -1)
        
        model = load_model()
    
        predicted_proba = model.predict(X_inference)[0]

        return jsonify({'winning_odds_home': predicted_proba})
