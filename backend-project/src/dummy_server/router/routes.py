from flask_restful import Api
import dummy_server.resources as res

API = "/api/"  # optional string


def add_routes(app):
    api = Api(app)

    api.add_resource(res.games_data.GamesResource, API + "games")
    api.add_resource(res.games_data.GamesResourceByID, API + "games/<game_id>")
    api.add_resource(res.games_data.GamesResourceByMatchUp, API + "games/<home_team_id>_<visitor_team_id>")
    api.add_resource(res.games_data.GamesResourceAggregatedByTeam, API + "teams/<int:team_id>")
    api.add_resource(res.clustering.GamesResourceClustering, API + "clustering")

    # add resources for predictions
    api.add_resource(res.prediction.GetPrediction, API + "prediction/<int:team_id_home>-<int:team_id_away>")

    # add resources for explainability
    api.add_resource(res.explainability.GetShapleyValues, API + "prediction/xai/<int:team_id_home>-<int:team_id_away>")

    return api
