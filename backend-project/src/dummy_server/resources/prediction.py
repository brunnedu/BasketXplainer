from flask_restful import Resource
from flask import jsonify

class GetPrediction(Resource):
    """Get the prediction btw two teams"""

    #TODO: THiS IS A PLACEHOLDER!!! Need to cahnge it later
    def get(self, team_id_home, team_id_away):
        """Get the winning odds for two teams."""
        prediction = {team_id_home: 0.5, team_id_away: 0.5}
        return jsonify(prediction)
