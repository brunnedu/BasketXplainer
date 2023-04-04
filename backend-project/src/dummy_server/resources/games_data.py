import os
import pandas as pd
from flask_restful import Resource
from flask import jsonify

DATA_ROOT = os.path.join(".", "data")
GAMES_FILE_NAME = "dataset_games.csv"
path_name = os.path.join(DATA_ROOT, GAMES_FILE_NAME)


class GamesResourceAggregatedByTeam(Resource):
    """Averaged statistics of each team in a given season. For query usage"""

    def get(self, team_id: int):
        # TODO: could have separate aggregations for whether team is home or away

        # load data
        data = pd.read_csv(path_name)

        # only use season 2021
        data = data[data['SEASON']==2021]

        # select team data for home and away games
        team_data = []
        for s in ['home', 'away']:
            df = data[data[f'TEAM_ID_{s}']==team_id]
            df = df[[col for col in df.columns if col.endswith(f'_{s}')]]
            df.columns = df.columns.str.rstrip(f'_{s}')
            team_data.append(df)

        # combine data
        team_data = pd.concat(team_data)
        # aggregate data by calculating mean
        team_data_agg = team_data.mean().to_frame().T

        return jsonify(team_data_agg.to_dict("records"))


class GamesResource(Resource):
    """Games resources."""

    def get(self):
        """Get for all the teams"""
        data = pd.read_csv(path_name)
        # Convert to dictionary
        return jsonify(data.to_dict("records"))


class GamesResourceByID(Resource):
    """Game given game id. For query usage"""

    def get(self, game_id):
        """Get for all the teams"""
        data = pd.read_csv(path_name)
        game_data = data[data["GAME_ID"] == int(game_id)]
        # Convert to dictionary
        return jsonify(game_data.to_dict("records"))


class GamesResourceByMatchUp(Resource):
    """Game given matchups. For query usage"""

    def get(self, home_team_id, visitor_team_id):
        data = pd.read_csv(path_name)
        home_data = data[data["HOME_TEAM_ID"] == int(home_team_id)]
        match_up_data = home_data[home_data["VISITOR_TEAM_ID"] == int(visitor_team_id)]
        return jsonify(match_up_data.to_dict("records"))
    