import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
#t-test
from scipy.stats import sem
from scipy.stats import t
from scipy.stats import ttest_ind

#load the 2019-2020 match report
match_data = pd.read_csv("Match Report/2019-2020_Match_data.csv")

#Show the percentage of home wins, away wins and draw
match_data["FR"].value_counts().plot(kind='pie', labels=["Home wins", "Away wins", "Draws"], autopct='%2.2f%%', explode=(0.01, 0.01, 0.01))
plt.title('Match results')
plt.show()



#Statistical t-test for the home x away wins
home_win = np.array(match_data['FR'].replace(to_replace=['H', 'A', 'D'], value=[1, 0, 0], inplace=False))
away_win = np.array(match_data['FR'].replace(to_replace=['H', 'A', 'D'], value=[0, 1, 0], inplace=False))

alpha = 0.05

t_stat, p = ttest_ind(home_win, away_win)
print(t_stat)
print(p)

def independent_ttest(data_1, data_2, alpha):
	#Mean of each data
	mean_1, mean_2 = np.mean(data_1), np.mean(data_2)
	#Calculate the degrees of freedom
	d_f = len(data_1) + len(data_2) - 2
	#Standard error of the mean
	se_1, se_2 = sem(data_1), sem(data_2)
	#Standard error of the difference between the standard error
	se_d = math.sqrt(se_1**2 + se_2**2)
	#Calculate the t statistic
	t_stat = (mean_1 - mean_2) / se_d
	#Calculate the critical value
	cv = t.ppf(1.0 - alpha, d_f)
	#Calculate the p-value
	p = (1.0 - t.cdf(abs(t_stat), d_f)) * 2.0
	#Return the t statistic, degrees of freedom, critical value and p-value of the test
	return t_stat, d_f, cv, p

t_stat, df, cv, p = independent_ttest(home_win, away_win, alpha)
print(t_stat)
print(df)
print(cv)
print(p)

if p > alpha:
	print("The means are equal")
else:
	print("The means are not equal")





#Statistical t-test for the home/ away wins for individual teams
teams = sorted(match_data["Team_1"].unique())
alpha = 0.05

for i in range(len(teams)):
	team_name = teams[i]
	print("### " + team_name + " ###")

	results = match_data.loc[match_data["Team_1"] == team_name]["FR"]
	home_win = np.array(results.replace(to_replace=['H', 'A', 'D'], value=[1, 0, 0], inplace=False))
	not_win = np.array(results.replace(to_replace=['H', 'A', 'D'], value=[0, 1, 1], inplace=False))

	t_stat, p = ttest_ind(home_win, not_win)
	# print(t_stat)
	# print(p)
	print(sum(home_win))

	if p > alpha:
		print("The means are equal")
	else:
		print("The means are not equal")




	results = match_data.loc[match_data["Team_2"] == team_name]["FR"]
	away_win = np.array(results.replace(to_replace=['H', 'A', 'D'], value=[0, 1, 0], inplace=False))
	not_win = np.array(results.replace(to_replace=['H', 'A', 'D'], value=[1, 0, 1], inplace=False))

	t_stat, p = ttest_ind(away_win, not_win)
	# print(t_stat)
	# print(p)
	print(sum(away_win))

	if p > alpha:
		print("The means are equal")
	else:
		print("The means are not equal")

	print("######")