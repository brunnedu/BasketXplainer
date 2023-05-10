from flask_restful import Resource
from flask import jsonify, request
import pandas as pd
from .utils import DATA_ROOT, load_model, load_tree_explainer
import shap

class GetSHAPForcePlotBoxscore(Resource):

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
        """Get the SHAP feature importance values based on the boxscore stats"""

        X_inference = pd.DataFrame({
            'AST_home': [AST_home],
            'BLK_home': [BLK_home],
            'DREB_home': [DREB_home],
            'FG3A_home': [FG3A_home],
            'FG3M_home': [FG3M_home],
            'FGA_home': [FGA_home],
            'FGM_home': [FGM_home],
            'FTA_home': [FTA_home],
            'FTM_home': [FTM_home],
            'OREB_home': [OREB_home],
            'PF_home': [PF_home],
            'STL_home': [STL_home],
            'TO_home': [TO_home],
            'AST_away': [AST_away],
            'BLK_away': [BLK_away],
            'DREB_away': [DREB_away],
            'FG3A_away': [FG3A_away],
            'FG3M_away': [FG3M_away],
            'FGA_away': [FGA_away],
            'FGM_away': [FGM_away],
            'FTA_away': [FTA_away],
            'FTM_away': [FTM_away],
            'OREB_away': [OREB_away],
            'PF_away': [PF_away],
            'STL_away': [STL_away],
            'TO_away': [TO_away]
        })


        explainer = load_tree_explainer()

        shap_values = explainer.shap_values(X_inference)

        force_plot = shap.force_plot(explainer.expected_value, shap_values[0], text_rotation=0, matplotlib=False, feature_names=X_inference.columns)

        shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"

        return shap_html
    