from flask_restful import Resource
from flask import jsonify

STATISTICS = ["2FG%", "3FG%", "Assists", "Rebounds"]

class GetShapleyValues(Resource):
    """Get the prediction btw two teams"""

    #TODO: THiS IS A PLACEHOLDER!!! Need to cahnge it later
    def get(self, team_id_home, team_id_away):
        """Get the winning odds for two teams."""
        prediction = {}
        for stat in STATISTICS:
            prediction[stat] = 2
        prediction["Average_score"] = 100
        prediction["Difference"] = 8
        return jsonify(prediction)