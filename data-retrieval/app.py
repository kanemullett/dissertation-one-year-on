import json
import os

from flask import Flask, Response, jsonify, make_response
from flask_restx import Api, Resource, reqparse

from fixture_set import FixtureSet

app = Flask(__name__)

api = Api(app, title="Data Retrieval Service Controller", version="0.0.1")

scrape = api.namespace("data-retrieval")

fixture_parser = reqparse.RequestParser()
fixture_parser.add_argument("month", type=str, required=True)
fixture_parser.add_argument("year", type=int, required=True)


@scrape.route("/fixtures")
class Fixtures(Resource):
    """

    """

    @scrape.expect(fixture_parser)
    @scrape.response(200, "OK")
    @scrape.response(400, "Bad Request")
    def get(self) -> Response:
        args = fixture_parser.parse_args()

        month = (args["month"]).lower()
        year = args["year"]

        accepted_months = ["october", "november", "december", "january", "february", "march", "april", "may", "june"]

        if month not in accepted_months:
            return make_response(jsonify("Invalid month selection."), 400)

        if year < 2014 or year > 2023:
            return make_response(jsonify("Invalid year selection."), 400)

        this_fixture_set = FixtureSet(month, str(year))
        this_fixture_dataframe = this_fixture_set.get_dataframe()

        fixtures = []

        row = 0
        while row < len(this_fixture_dataframe):
            fixtures.append({
                "date": this_fixture_dataframe["Date"][row],
                "tipOffTime": this_fixture_dataframe["Tip-Off Time"][row],
                "awayTeam": this_fixture_dataframe["Away Team"][row],
                "awayPoints": int(this_fixture_dataframe["Away PTS"][row]),
                "homeTeam": this_fixture_dataframe["Home Team"][row],
                "homePoints": int(this_fixture_dataframe["Home PTS"][row]),
                "attendance": this_fixture_dataframe["Attendance"][row]
            })
            row += 1

        final_object = {
            "month": month,
            "year": year,
            "fixtureCount": len(fixtures),
            "fixtures": fixtures
        }

        return Response(json.dumps(final_object), mimetype="application/json", status=200)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
