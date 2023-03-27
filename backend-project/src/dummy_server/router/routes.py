from flask_restful import Api
import dummy_server.resources as res

API = "/api/data/"  # optional string


def add_routes(app):
    api = Api(app)

    api.add_resource(res.games_data.GamesResource, API + "games")
    api.add_resource(res.games_data.GamesResourceByID, API + "games/<game_id>")
    api.add_resource(res.games_data.GamesResourceByMatchUp, API + "games/<home_team_id>_<visitor_team_id>")

    return api
