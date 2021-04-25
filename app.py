import os 

from nba_api.stats.endpoints import commonplayerinfo, shotchartdetail
from nba_api.stats.static import players, teams
from nba_api.stats.library.parameters import * 

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import json 


# Flask app
app = Flask(__name__, static_url_path="", template_folder="templates")
# app._static_folder = os.path.abspath("static")


all_teams = teams.get_teams()
all_players = players.get_active_players()


# Map team name to team id 
team_ids = {
	team["full_name"]: team["id"] for team in all_teams 
}

# Map player name to player id 
player_ids = {
	player["full_name"]: player["id"] for player in all_players
}


@app.route("/team", methods=["GET", "POST"])
def handle_team():	
	if request.method == "GET":
		data = {
			"time_type": None,
			"date_from": None,
			"date_to": None, 
			"season": None,
			"location": None,
			"conference": None,
			"team_name": None,
			"team_abbr": None,
			"shot_chart": None,
			"team_average": None,
			"league_average": None,
			"other_averages": None
		}

	if request.method == "POST":
		team_name = request.form["teamSelect"][:-6]
		team_abbr = request.form["teamSelect"][-4:-1]
		team_id = team_ids[team_name]

		date_from, date_to = "", ""
		season = SeasonNullable.default
		time_type = request.form["timeSelect"]
		if time_type == "Season":
			season = request.form["seasonSelect"][:7]
		elif time_type == "Time Period":
			date_from = request.form["timeStart"]
			date_to = request.form["timeEnd"]
		else:
			raise ValueError("Invalid time type")

		location_input = request.form.getlist("location")
		if len(location_input) == 0 or len(location_input) == 2:
			location = LocationNullable.default
		else:
			if location_input[0] == "home":
				location = "Home"
			else:
				location = "Road"

		conference_input = request.form.getlist("conference")
		if len(conference_input) == 0 or len(conference_input) == 2:
			conference = ConferenceNullable.default
		else:
			if conference_input[0] == "westOppt":
				conference = "West"
			else:
				conference = "East"

		team_chart, team_average, league_average, other_averages = get_team_data(
			team_id=team_id,
			player_id=0,
			date_from=date_from,
			date_to=date_to,
			season=season,
			season_type="Regular Season",
			location=location,
			vs_conference=conference,
			context_measure_simple="FGA"
		)

		# Change text to display
		if location == "Road":
			location = "Away"

		data = {
			"time_type": time_type,
			"date_from": date_from, 
			"date_to": date_to, 
			"season": season,
			"location": location if location != LocationNullable.default else None,
			"conference": conference if conference != ConferenceNullable.default else None,
			"team_name": team_name,
			"team_abbr": team_abbr,
			"shot_chart": team_chart,
			"team_average": team_average,
			"league_average": league_average,
			"other_averages": other_averages	
		}

	return render_template("team.html", all_teams=all_teams, all_players=all_players, data=data)


@app.route("/player", methods=["GET", "POST"])
def handle_player():	
	if request.method == "GET":
		data = {
			"time_type": None,
			"date_from": None,
			"date_to": None, 
			"season": None,
			"location": None,
			"conference": None,
			"player_name": None,
			"shot_chart": None,
			"team_average": None,
			"league_average": None,
			"other_averages": None
		}

	if request.method == "POST":
		player_name = request.form["playerSelect"]
		player_id = player_ids[player_name]

		date_from, date_to = "", ""
		season = SeasonNullable.default
		time_type = request.form["timeSelect"]
		if time_type == "Season":
			season = request.form["seasonSelect"][:7]
		elif time_type == "Time Period":
			date_from = request.form["timeStart"]
			date_to = request.form["timeEnd"]
		else:
			raise ValueError("Invalid time type")

		location_input = request.form.getlist("location")
		if len(location_input) == 0 or len(location_input) == 2:
			location = LocationNullable.default
		else:
			if location_input[0] == "home":
				location = "Home"
			else:
				location = "Road"

		conference_input = request.form.getlist("conference")
		if len(conference_input) == 0 or len(conference_input) == 2:
			conference = ConferenceNullable.default
		else:
			if conference_input[0] == "westOppt":
				conference = "West"
			else:
				conference = "East"

		team_chart, team_average, league_average, other_averages = get_team_data(
			team_id=team_id,
			player_id=0,
			date_from=date_from,
			date_to=date_to,
			season=season,
			season_type="Regular Season",
			location=location,
			vs_conference=conference,
			context_measure_simple="FGA"
		)

		# Change text to display
		if location == "Road":
			location = "Away"

		data = {
			"time_type": time_type,
			"date_from": date_from, 
			"date_to": date_to, 
			"season": season,
			"location": location if location != LocationNullable.default else None,
			"conference": conference if conference != ConferenceNullable.default else None,
			"team_name": team_name,
			"team_abbr": team_abbr,
			"shot_chart": team_chart,
			"team_average": team_average,
			"league_average": league_average,
			"other_averages": other_averages	
		}

	return render_template("team.html", all_teams=all_teams, all_players=all_players, data=data)

	return render_template("player.html", all_teams=all_teams, all_players=all_players, data=data)

def get_team_data(
	team_id, 
	player_id=0, 
	date_from="", 
	date_to="", 
	season=SeasonNullable.default,
	season_type="Regular Season",
	location=LocationNullable.default,
	vs_conference=ConferenceNullable.default,
	context_measure_simple="FGA"
	):
	"""
	0 GRID_TYPE
	1 GAME_ID
	2 GAME_EVENT_ID
	3 PLAYER_ID
	4 PLAYER_NAME
	5 TEAM_ID
	6 TEAM_NAME
	7 PERIOD
	8 MINUTES_REMAINING
	9 SECONDS_REMAINING
	10 EVENT_TYPE
	11 ACTION_TYPE
	12 SHOT_TYPE
	13 SHOT_ZONE_BASIC
	14 SHOT_ZONE_AREA
	15 SHOT_ZONE_RANGE
	16 SHOT_DISTANCE
	17 LOC_X
	18 LOC_Y
	19 SHOT_ATTEMPTED_FLAG 
	20 SHOT_MADE_FLAG
	21 GAME_DATE
	22 HTM
	23 VTM
	"""
	shot_chart = shotchartdetail.ShotChartDetail(
		team_id=team_id,
		player_id=player_id,
		date_from_nullable=date_from, 
		date_to_nullable=date_to,
		season_nullable=season,
		season_type_all_star=season_type,
		location_nullable=location,
		vs_conference_nullable=vs_conference,
		context_measure_simple=context_measure_simple
	) 
	shot_array = shot_chart.get_dict()["resultSets"][0]["rowSet"]

	# Compute team average 
	team_average = get_team_average(convert_to_df(shot_chart.get_dict()["resultSets"][0]))
	# Compute league average 
	league_average = get_league_average(convert_to_df(shot_chart.get_dict()["resultSets"][1]))

	# Compute other teams' individual averages
	other_averages = {}
	for other_team, other_id in team_ids.items():
		if other_id == team_id:
			continue 
		else:
			print(other_team)
			"""
			other_shot_chart = shotchartdetail.ShotChartDetail(
				team_id=other_id,
				player_id=player_id,
				date_from_nullable=date_from, 
				date_to_nullable=date_to,
				season_nullable=season,
				season_type_all_star=season_type,
				location_nullable=location,
				vs_conference_nullable=vs_conference,
				context_measure_simple=context_measure_simple
			) 
			other_averages[other_team] = get_team_average(convert_to_df(other_shot_chart.get_dict()["resultSets"][0]))
			"""

	return shot_array, team_average, league_average, other_averages


def get_team_average(df):
	three_point_zone = ["Above the Break 3", "Backcourt", "Left Corner 3", "Right Corner 3"]

	two_point_fga = len(df.loc[(~df["SHOT_ZONE_BASIC"].isin(three_point_zone))])
	two_point_fgm = len(df.loc[(~df["SHOT_ZONE_BASIC"].isin(three_point_zone)) & (df["EVENT_TYPE"] == "Made Shot")])
	two_point_fg_pcg = round(two_point_fgm / two_point_fga * 100, 2)

	three_point_fga = len(df.loc[df["SHOT_ZONE_BASIC"].isin(three_point_zone)])
	three_point_fgm = len(df.loc[df["SHOT_ZONE_BASIC"].isin(three_point_zone) & (df["EVENT_TYPE"] == "Made Shot")])
	three_point_fg_pcg = round(three_point_fgm / three_point_fga * 100, 2)

	total_fga = two_point_fga + three_point_fga 
	total_fgm = two_point_fgm + three_point_fgm
	total_fg_pcg = round(total_fgm / total_fga * 100, 2)

	return {
		"two_point": {
			"FGA": two_point_fga,
			"FGM": two_point_fgm,
			"FG_PCT": two_point_fg_pcg
		},
		"three_point": {
			"FGA": three_point_fga,
			"FGM": three_point_fgm,
			"FG_PCT": three_point_fg_pcg
		},
		"total": {
			"FGA": total_fga,
			"FGM": total_fgm,
			"FG_PCT": total_fg_pcg
		}
	}


def get_league_average(df):
	three_point_zone = ["Above the Break 3", "Backcourt", "Left Corner 3", "Right Corner 3"]

	two_point_fga = df.loc[~df["SHOT_ZONE_BASIC"].isin(three_point_zone), "FGA"].sum()
	two_point_fgm = df.loc[~df["SHOT_ZONE_BASIC"].isin(three_point_zone), "FGM"].sum()
	two_point_fg_pcg = round(two_point_fgm / two_point_fga * 100, 2)
	three_point_fga = df.loc[df["SHOT_ZONE_BASIC"].isin(three_point_zone), "FGA"].sum()
	three_point_fgm = df.loc[df["SHOT_ZONE_BASIC"].isin(three_point_zone), "FGM"].sum()
	three_point_fg_pcg = round(three_point_fgm / three_point_fga * 100, 2)

	total_fga = two_point_fga + three_point_fga 
	total_fgm = two_point_fgm + three_point_fgm
	total_fg_pcg = round(total_fgm / total_fga * 100, 2)

	return {
		"two_point": {
			"FGA": two_point_fga,
			"FGM": two_point_fgm,
			"FG_PCT": two_point_fg_pcg
		},
		"three_point": {
			"FGA": three_point_fga,
			"FGM": three_point_fgm,
			"FG_PCT": three_point_fg_pcg
		},
		"total": {
			"FGA": total_fga,
			"FGM": total_fgm,
			"FG_PCT": total_fg_pcg
		}
	}

def convert_to_df(data):
	df = pd.DataFrame(data["rowSet"], columns=data["headers"])
	return df 


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)
