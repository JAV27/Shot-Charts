from nba_api.stats.endpoints import commonplayerinfo, shotchartdetail
from nba_api.stats.static import players, teams
import pandas as pd
import numpy as np
import json 

teams = teams.get_teams()

team_ids = []
for i in teams:
	team_ids.append(i['id'])

sc = shotchartdetail.ShotChartDetail(team_id=1610612762,
	player_id=0,
	season_nullable='2018-19',
	season_type_all_star='Regular Season',	
    context_measure_simple='FGA')

arr = sc.get_dict()['resultSets'][0]['rowSet']
print(arr[1])


players = players.get_players()
player_ids = []

player_info = commonplayerinfo.CommonPlayerInfo(player_id=202399)

for i in players:
	player_ids.append(i['id'])		

def getRelevant(n):
	return [n[3],n[5],n[10],n[12],n[14],n[17],n[18]]

total_data = []
for i in team_ids:
	sc = shotchartdetail.ShotChartDetail(team_id=i,
		player_id=0,
		season_nullable='2018-19',
		season_type_all_star='Regular Season',	
		context_measure_simple='FGA')

	arr = sc.get_dict()['resultSets'][0]['rowSet']
	filtered = map(getRelevant, arr)
	total_data.append(list(filtered))
	print(str(i) + " is done!")

with open('shots.json', 'w') as fp:
    json.dump(total_data, fp)