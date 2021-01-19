import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

match_data = pd.read_csv("serie a/2020-2021_Match_data.csv")

teams = sorted(match_data["Team_1"].unique())
teams_goals_scored_home = {}
teams_goals_scored_away = {}
teams_goals_scored = {}
teams_shots_home = {}
teams_shots_away = {}
teams_shots = {}

teams_games = {}
teams_games_home = {}
teams_games_away = {}

for i in range(len(teams)):
	results_1 = match_data.loc[(match_data["Team_1"] == teams[i]), "Gls_T1"].sum()
	teams_goals_scored_home[teams[i]] = results_1
	results_2 = match_data.loc[(match_data["Team_2"] == teams[i]), "Gls_T2"].sum()
	teams_goals_scored_away[teams[i]] = results_2
	teams_goals_scored[teams[i]] = results_1 + results_2

	results_1 = match_data.loc[(match_data["Team_1"] == teams[i]), "Atp_T1"].sum()
	teams_shots_home[teams[i]] = results_1
	results_2 = match_data.loc[(match_data["Team_2"] == teams[i]), "Atp_T2"].sum()
	teams_shots_away[teams[i]] = results_2
	teams_shots[teams[i]] = results_1 + results_2

	matches = match_data.loc[(match_data["Team_1"] == teams[i]) | (match_data["Team_2"] == teams[i]), "Ptt"].count()
	teams_games[teams[i]] = matches
	matches = match_data.loc[(match_data["Team_1"] == teams[i]), "Ptt"].count()
	teams_games_home[teams[i]] = matches
	matches = match_data.loc[(match_data["Team_2"] == teams[i]), "Ptt"].count()
	teams_games_away[teams[i]] = matches

from PIL import Image
def getImage(path):
	img = Image.open(path)
	img = img.resize((20,20))
	return OffsetImage(img)

##Home/away
data_team = []
data_points_x = []
data_points_y = []
for i in range(len(teams)):
	data_team.append("serie a/serie a logo/" + teams[i].lower() + ".png")
	data_points_x.append(teams_goals_scored[teams[i]] / teams_shots[teams[i]])
	data_points_y.append(teams_shots[teams[i]] / teams_games[teams[i]])#38.)

fig, ax = plt.subplots()
ax.set_title('Attack efficiency home/away')
ax.set_xlabel('Conversion rate (%)')
ax.set_ylabel('Avg shots per game')
ax.scatter(data_points_x, data_points_y, color=['#FFFFFF'])

for x0, y0, path in zip(data_points_x, data_points_y, data_team):
	ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
	ax.add_artist(ab)

plt.show()


##Home
data_team = []
data_points_x = []
data_points_y = []
for i in range(len(teams)):
	data_team.append("serie a/serie a logo/" + teams[i].lower() + ".png")
	data_points_x.append(teams_goals_scored_home[teams[i]] / teams_shots_home[teams[i]])
	data_points_y.append(teams_shots_home[teams[i]] / teams_games_home[teams[i]])#19.)

fig, ax = plt.subplots()
ax.set_title('Attack efficiency home')
ax.set_xlabel('Conversion rate (%)')
ax.set_ylabel('Avg shots per game')
ax.scatter(data_points_x, data_points_y, color=['#FFFFFF'])

for x0, y0, path in zip(data_points_x, data_points_y, data_team):
	ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
	ax.add_artist(ab)

plt.show()


##Away
data_team = []
data_points_x = []
data_points_y = []
for i in range(len(teams)):
	data_team.append("serie a/serie a logo/" + teams[i].lower() + ".png")
	data_points_x.append(teams_goals_scored_away[teams[i]] / teams_shots_away[teams[i]])
	data_points_y.append(teams_shots_away[teams[i]] / teams_games_away[teams[i]])#19.)

fig, ax = plt.subplots()
ax.set_title('Attack efficiency away')
ax.set_xlabel('Conversion rate (%)')
ax.set_ylabel('Avg shots per game')
ax.scatter(data_points_x, data_points_y, color=['#FFFFFF'])

for x0, y0, path in zip(data_points_x, data_points_y, data_team):
	ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
	ax.add_artist(ab)

plt.show()