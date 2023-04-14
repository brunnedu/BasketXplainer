import os
import pandas as pd
from flask_restful import Resource
from flask import jsonify
from flask import send_file
from .utils import DATA_ROOT, DATA_ROOT_FROM_ROUTER, PRED_COLS


class GetTeamBoxscore(Resource):
    """Averaged statistics of each team in a given season. For query usage"""

    def get(self, team_id: int, is_home: int):
        # TODO: could have separate aggregations for whether team is home or away

        boxscores = pd.read_csv(os.path.join(DATA_ROOT, 'precomputed', 'boxscores.csv'), index_col=0)

        # filter precomputed boxscores
        team_boxscore = boxscores[(boxscores['TEAM_ID']==team_id) & (boxscores['is_home']==is_home)][PRED_COLS]

        return jsonify(team_boxscore.to_dict("records"))
    

class GetTeamLogo(Resource):
    """Get team logo for any team ID"""

    def get(self, team_id: int):
        path = os.path.join(DATA_ROOT_FROM_ROUTER, "team_logos", f"{team_id}.png")
        return send_file(path, mimetype="image/png")
    

class GetTeams(Resource):
    """Get all team_ids"""

    def get(self):

        # load data
        games = pd.read_csv(os.path.join(DATA_ROOT, "dataset_games.csv"))
        teams = pd.read_csv(os.path.join(DATA_ROOT, "dataset_teams.csv"))

        # only use season 2021
        games = games[games['SEASON']==2021]
        team_info = teams[teams['TEAM_ID'].isin(games['TEAM_ID_home'].unique())]

        # add name column that concatenates city with nickname
        team_info['name'] = team_info.apply(lambda row: f"{row['CITY']} {row['NICKNAME']}", axis=1)

        # return team_id and name
        return jsonify(team_info[['TEAM_ID', 'name']].to_dict('records'))
    