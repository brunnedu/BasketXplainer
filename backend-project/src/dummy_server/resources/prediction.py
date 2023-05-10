import numpy as np
from flask import jsonify
from flask_restful import Resource

from .utils import PRED_COLS, load_model, load_new_stat_classifier

class GetPredictionTeam(Resource):
    """Get the prediction btw two teams"""

    #TODO: THiS IS A PLACEHOLDER!!! Need to cahnge it later
    def get(self, team_id_home, team_id_away):
        """Get the winning odds for two teams."""
        
        return jsonify({'winning_odds_home': 0.37})
    

class GetPredictionBoxscore(Resource):

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
        """Get the predicted winning odds of the home team based on the boxscore stats"""

        # TODO: load model and perform inference

        X_inference = np.array([
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
        ]).reshape(1, -1)
        
        model = load_model()
    
        predicted_proba = model.predict(X_inference)[0]

        return jsonify({'winning_odds_home': predicted_proba})
    
    
class GetPredictionBoxscoreNewStats(Resource):

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
        """Get the predicted winning odds of the home team based on the boxscore stats"""

        # TODO: load model and perform inference

        X_inference = np.array([
            AST_home, 
            BLK_home,
            DREB_home, 
            OREB_home, 
            STL_home, 
            FGA_home,
            FG3A_home, 
            FTA_home,
            TO_home, 
            AST_away, 
            BLK_away, 
            DREB_away,
            OREB_away, 
            STL_away, 
            FGA_away, 
            FG3A_away, 
            FTA_away, 
            TO_away
        ]).reshape(1, -1)
        
        model = load_new_stat_classifier()
    
        predicted_proba = model.predict(X_inference)[0]

        return jsonify({'winning_odds_home': predicted_proba})

