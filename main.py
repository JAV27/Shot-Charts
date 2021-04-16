from nba_api.stats.endpoints import commonplayerinfo, shotchartdetail
from nba_api.stats.static import players
import pandas as pd
import numpy as np

players = players.get_players()

player_info = commonplayerinfo.CommonPlayerInfo(player_id=players[1]['id'])

sc = shotchartdetail.ShotChartDetail(team_id=0,
	player_id=201935,
	season_nullable='2018-19',
	season_type_all_star='Regular Season',
    context_measure_simple='FGA')

arr = sc.get_data_frames()[0]

print("All shots for James Harden in 2018")
print(arr.iloc[:,17:19])

