import dummy_server.resources as res
from flask_restful import Api

API = "/api/"  # optional string


def add_routes(app):
    api = Api(app)

    api.add_resource(res.games_data.GetTeamLogo, API + "logo/<int:team_id>")

    api.add_resource(res.games_data.GetTeams, API + "teams")
    api.add_resource(res.games_data.GetTeamBoxscore, API + "boxscore/<int:team_id>-<int:is_home>")
    api.add_resource(res.games_data.GetBoxscoreBounds, API + "boxscore/bounds")
    api.add_resource(res.games_data.GetBoxscoresHome, API + "boxscores/home")
    api.add_resource(res.games_data.GetBoxscoresAway, API + "boxscores/away")

    api.add_resource(res.clustering.GetClusteringTeam, API + "clustering/teams")
    api.add_resource(res.prediction.GetPredictionTeam, API + "prediction/teams/<int:team_id_home>-<int:team_id_away>")
    api.add_resource(res.explainability.GetSHAPValuesTeam, API + "shap/teams/<int:team_id_home>-<int:team_id_away>")

    api.add_resource(res.clustering.GetClusteringBoxscore, API + "clustering/<float:AST_home>-<float:BLK_home>-<float:DREB_home>-<float:FG3A_home>-<float:FG3M_home>-<float:FGA_home>-<float:FGM_home>-<float:FTA_home>-<float:FTM_home>-<float:OREB_home>-<float:PF_home>-<float:STL_home>-<float:TO_home>_<float:AST_away>-<float:BLK_away>-<float:DREB_away>-<float:FG3A_away>-<float:FG3M_away>-<float:FGA_away>-<float:FGM_away>-<float:FTA_away>-<float:FTM_away>-<float:OREB_away>-<float:PF_away>-<float:STL_away>-<float:TO_away>")
    api.add_resource(res.prediction.GetPredictionBoxscore, API + "prediction/<float:AST_home>-<float:BLK_home>-<float:DREB_home>-<float:FG3A_home>-<float:FG3M_home>-<float:FGA_home>-<float:FGM_home>-<float:FTA_home>-<float:FTM_home>-<float:OREB_home>-<float:PF_home>-<float:STL_home>-<float:TO_home>_<float:AST_away>-<float:BLK_away>-<float:DREB_away>-<float:FG3A_away>-<float:FG3M_away>-<float:FGA_away>-<float:FGM_away>-<float:FTA_away>-<float:FTM_away>-<float:OREB_away>-<float:PF_away>-<float:STL_away>-<float:TO_away>")
    api.add_resource(res.explainability.GetSHAPForcePlotBoxscore, API + "shap/<float:AST_home>-<float:BLK_home>-<float:DREB_home>-<float:FG3A_home>-<float:FG3M_home>-<float:FGA_home>-<float:FGM_home>-<float:FTA_home>-<float:FTM_home>-<float:OREB_home>-<float:PF_home>-<float:STL_home>-<float:TO_home>_<float:AST_away>-<float:BLK_away>-<float:DREB_away>-<float:FG3A_away>-<float:FG3M_away>-<float:FGA_away>-<float:FGM_away>-<float:FTA_away>-<float:FTM_away>-<float:OREB_away>-<float:PF_away>-<float:STL_away>-<float:TO_away>")

    return api
