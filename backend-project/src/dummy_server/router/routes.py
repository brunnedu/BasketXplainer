from flask_restful import Api
import dummy_server.resources as res

API = "/api/"  # optional string


def add_routes(app):
    api = Api(app)

    api.add_resource(res.games_data.GetTeams, API + "teams")
    api.add_resource(res.games_data.GetTeamBoxscore, API + "boxscore/<int:team_id>-<int:is_home>")

    api.add_resource(res.clustering.GetClusteringTeam, API + "clustering/teams")
    api.add_resource(res.prediction.GetPredictionTeam, API + "prediction/teams/<int:team_id_home>-<int:team_id_away>")
    api.add_resource(res.explainability.GetShapleyValuesTeam, API + "feature_importance/teams/<int:team_id_home>-<int:team_id_away>")

    api.add_resource(res.clustering.GetClusteringBoxscore, API + "clustering/<float:FGM_home>-<float:FGA_home>-<float:FG3M_home>-<float:FG3A_home>-<float:FTM_home>-<float:FTA_home>-<float:OREB_home>-<float:DREB_home>-<float:AST_home>-<float:STL_home>-<float:BLK_home>-<float:TO_home>-<float:PF_home>_<float:FGM_away>-<float:FGA_away>-<float:FG3M_away>-<float:FG3A_away>-<float:FTM_away>-<float:FTA_away>-<float:OREB_away>-<float:DREB_away>-<float:AST_away>-<float:STL_away>-<float:BLK_away>-<float:TO_away>-<float:PF_away>")
    api.add_resource(res.prediction.GetPredictionBoxscore, API + "prediction/<float:FGM_home>-<float:FGA_home>-<float:FG3M_home>-<float:FG3A_home>-<float:FTM_home>-<float:FTA_home>-<float:OREB_home>-<float:DREB_home>-<float:AST_home>-<float:STL_home>-<float:BLK_home>-<float:TO_home>-<float:PF_home>_<float:FGM_away>-<float:FGA_away>-<float:FG3M_away>-<float:FG3A_away>-<float:FTM_away>-<float:FTA_away>-<float:OREB_away>-<float:DREB_away>-<float:AST_away>-<float:STL_away>-<float:BLK_away>-<float:TO_away>-<float:PF_away>")
    api.add_resource(res.explainability.GetShapleyValuesBoxscore, API + "feature_importance/<float:FGM_home>-<float:FGA_home>-<float:FG3M_home>-<float:FG3A_home>-<float:FTM_home>-<float:FTA_home>-<float:OREB_home>-<float:DREB_home>-<float:AST_home>-<float:STL_home>-<float:BLK_home>-<float:TO_home>-<float:PF_home>_<float:FGM_away>-<float:FGA_away>-<float:FG3M_away>-<float:FG3A_away>-<float:FTM_away>-<float:FTA_away>-<float:OREB_away>-<float:DREB_away>-<float:AST_away>-<float:STL_away>-<float:BLK_away>-<float:TO_away>-<float:PF_away>")

    return api
