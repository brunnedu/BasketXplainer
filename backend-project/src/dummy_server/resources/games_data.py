import os
import pandas as pd
from flask_restful import Resource

DATA_ROOT = os.path.join(".", "data")
GAMES_FILE_NAME = "dataset_games.csv"
path_name = os.path.join(DATA_ROOT, GAMES_FILE_NAME)

class GamesResource(Resource):
    """Games resources."""

    def get(self):
        """Get for all the teams"""
        data = pd.read_csv(path_name)
        # Convert to dictionary
        return data.to_dict("records")

class GamesResourceByID(Resource):
    """Game given game id. For query usage"""

    def get(self, game_id):
        """Get for all the teams"""
        data = pd.read_csv(path_name)
        game_data = data[data["GAME_ID"] == int(game_id)]
        # Convert to dictionary
        return game_data.to_dict("records")
    
class GamesResourceByMatchUp(Resource):
    """Game given matchups. For query usage"""

    def get(self, home_team_id, visitor_team_id):
        data = pd.read_csv(path_name)
        home_data = data[data["HOME_TEAM_ID"] == int(home_team_id)]
        match_up_data = home_data[home_data["VISITOR_TEAM_ID"] == int(visitor_team_id)]
        return match_up_data.to_dict("records")


    
