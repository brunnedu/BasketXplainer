import os

import pandas as pd
from flask import jsonify, make_response, send_file
from flask_restful import Resource

from .utils import DATA_ROOT, PRED_COLS


class GetTeamBoxscore(Resource):
    """Averaged statistics of each team in a given season. For query usage"""

    def get(self, team_id: int, is_home: int):
        # TODO: could have separate aggregations for whether team is home or away

        boxscores = pd.read_csv(os.path.join(DATA_ROOT, 'precomputed', 'boxscores.csv'), index_col=0)

        # filter precomputed boxscores
        team_boxscore = boxscores[(boxscores['TEAM_ID']==team_id) & (boxscores['is_home']==is_home)][PRED_COLS]

        return jsonify(team_boxscore.to_dict("records"))
    

class GetBoxscoresHome(Resource):
    """Averaged statistics of each team in a given season. For query usage"""

    def get(self):
        # TODO: could have separate aggregations for whether team is home or away

        boxscores = pd.read_csv(os.path.join(DATA_ROOT, 'precomputed', 'boxscores.csv'), index_col=0)

        # filter precomputed boxscores
        home_boxscores = boxscores[boxscores['is_home']][PRED_COLS]

        # build csv response
        csv = home_boxscores.to_csv(index=False)

        response = make_response(csv)
        response.headers['Content-Disposition'] = 'attachment; filename=boxscores_home.csv'
        response.headers['Content-Type'] = 'text/csv'

        return response
    

class GetBoxscoresAway(Resource):
    """Averaged statistics of each team in a given season. For query usage"""

    def get(self):
        # TODO: could have separate aggregations for whether team is home or away

        boxscores = pd.read_csv(os.path.join(DATA_ROOT, 'precomputed', 'boxscores.csv'), index_col=0)

        # filter precomputed boxscores
        away_boxscores = boxscores[~boxscores['is_home']][PRED_COLS]

        # build csv response
        csv = away_boxscores.to_csv(index=False)

        response = make_response(csv)
        response.headers['Content-Disposition'] = 'attachment; filename=boxscores_away.csv'
        response.headers['Content-Type'] = 'text/csv'

        return response
    

class GetTeamLogo(Resource):
    """Get team logo for any team ID"""

    def get(self, team_id: int):
        path = os.path.join(DATA_ROOT, "team_logos", f"{team_id}.png")
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
    

class GetBoxscoreBounds(Resource):
    """Get lower and upper bounds for boxscore stats"""

    def get(self):
        
        # load precompouted boxscores
        boxscores = pd.read_csv(os.path.join(DATA_ROOT, 'precomputed', 'boxscores.csv'), index_col=0)

        # calculate min and max and add a buffer of half a standard deviation
        mins = boxscores.min()-0.5*boxscores.std()
        maxs = boxscores.max()+0.5*boxscores.std()

        bounds = {
            col: [mins[col], maxs[col]] for col in PRED_COLS
        }

        return jsonify(bounds)
    