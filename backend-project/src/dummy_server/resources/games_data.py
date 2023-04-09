import os
import pandas as pd
from flask_restful import Resource
from flask import jsonify

DATA_ROOT = os.path.join(".", "data")


class GetTeamBoxscore(Resource):
    """Averaged statistics of each team in a given season. For query usage"""

    def get(self, team_id: int, is_home: int):
        # TODO: could have separate aggregations for whether team is home or away

        # cols that make up boxscore stats
        BOXSCORE_COLS = ['FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TO', 'PF']

        # load data
        games = pd.read_csv(os.path.join(DATA_ROOT, "dataset_games.csv"))
        games_details = pd.read_csv(os.path.join(DATA_ROOT, "dataset_games_details.csv"))

        # only keep important cols
        games = games[['GAME_DATE_EST', 'GAME_ID', 'GAME_STATUS_TEXT', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'SEASON']]
        # join games to games_details for date information
        games_details = games_details.merge(games, on='GAME_ID')

        # add additional column indicating whether team is home or not
        games_details['is_home'] = games_details['TEAM_ID'] == games_details['HOME_TEAM_ID']
        games_details['date'] = pd.to_datetime(games_details['GAME_DATE_EST'])

        # only use games during regular season (lasted from 19.10.2021 until 10.04.2022)
        games_details = games_details[(pd.Timestamp('2021-10-19') <= games_details['date']) & (games_details['date'] <= pd.Timestamp('2022-04-10'))]

        # select data from team at home or away
        games_details = games_details[(games_details['TEAM_ID']==team_id) & (games_details['is_home']==is_home)][BOXSCORE_COLS+['GAME_ID']]

        # sum over all players for each game and then average over all games
        boxscore = games_details.groupby(['GAME_ID']).sum().mean().to_frame().T

        return jsonify(boxscore.to_dict("records"))
    

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
    