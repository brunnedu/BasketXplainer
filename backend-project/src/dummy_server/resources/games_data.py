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
    
class GamesResourceAggregatedBySeason(Resource):
    """Averaged statistics of each team in a given season. For query usage"""

    def get(self, season: int):
        data = pd.read_csv(path_name)
        # select data from season
        data_season = data[data['SEASON']==season]

        # calculate for every team their average statistics
        data_teams = []
        for team_id in data_season['TEAM_ID_home'].unique():
            curr_team_data = []
            # do same selection for both home & away games
            for s in ['home', 'away']:
                df = data_season[data_season[f'TEAM_ID_{s}']==team_id]
                df = df[[col for col in df.columns if col.endswith(f'_{s}')]]
                df.columns = df.columns.str.rstrip(f'_{s}')
                curr_team_data.append(df)
            
            curr_team_data = pd.concat(curr_team_data)
            # aggregate data using mean()
            curr_team_data_agg = curr_team_data.mean().to_frame().T
            curr_team_data_agg['TEAM_ID'] = curr_team_data_agg['TEAM_ID'].astype(int)
            data_teams.append(curr_team_data_agg)
        
        # combine aggregate stats of all teams
        data_teams = pd.concat(data_teams)
        return data_teams.to_dict("records")


    
