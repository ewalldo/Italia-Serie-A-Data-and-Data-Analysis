# Italia-Serie-A-Data-and-Data-Analysis  
Repository to hold the match data for Italia's Serie A and some analysis based on that.  

Match data for the 2019-2020 is already available  
Player data for the 2019-2020 is already available

(soon) TODO: Match data for previous seasons  
(soon) TODO: Player data for previous seasons  
(soon) TODO: More statistical analysis  


## 1 - Does home-field advantage matter? Does the home team wins more in Italia's Serie A?  
If you ask someone randomly on the street, the answer will probably be *"Of course, it does matter. Home teams will be playing in a familiar place, they will have the majority of the support from the stands and also don't need to travel to get there. They do have an advantage."* and their answer is not wrong, playing at home gives some psychological and physical advantages to the home team. That's why everyone wants to play the second leg of a knockout tournment at home, that advantage in the most important game can decide which team qualifies and which one drops out from the competition.  

[Looking at the data from England](https://www.skysports.com/football/news/11096/10955089/sky-sports-bust-common-football-myths-home-advantage), home-field advantage is something that exists since 1895, where the home-team would win 64.6% of the time, and even though it has been decreasing since them, it never went below 40%. Home-field advantage it is indeed a thing, but the main question is, does it happens in Italian football (more specifically the Serie A 2019-2020 season)? I will try to answer this question.  

First we simply count the results for the 2019-2020 and plot using a pie chart using pandas and matplotlib.
```
match_data = pd.read_csv("Match Report/2019-2020_Match_data.csv")
match_data["FR"].value_counts().plot(kind='pie', labels=["Home wins", "Away wins", "Draws"], autopct='%2.2f%%', explode=(0.01, 0.01, 0.01))
```
The result can be seen on the image below.  
<img src="/imgs/home_wins_pie.png" width="400">  
41.58% of the matches ended up with a home-win, that's no much different from England's Premier League. To be more precise, from the 380 matches played, 158 ended up with a home win, 137 with a away win and 85 with a draw. There were 21 (or 5.53% difference) more home than away wins, so the question now becomes *"Looking only at the 2019-2020 season, are these 21 more home wins statistically significant? Can we say for sure that home teams has won more than away teams for that season in particular?"* Let's apply some statistics to answer this question.  

For that we use Student's t-Test to see if the means of the two samples (home-win and away-win rate) are the same. First we set our null (H<sub>&theta;</sub>) and alternative (H<sub>1</sub>) hypotesis.  
H<sub>&theta;</sub>: &micro;<sub>1</sub> = &micro;<sub>2</sub>  
H<sub>1</sub>: &micro;<sub>1</sub> ≠ &micro;<sub>2</sub>  

For our significance level, we pick &alpha; = 0.05 (i.e. the probability of we rejecting the null hypothesis when it's true, by picking a value of 0.05 we assume a risk of 5% of concluding that a difference exists when there is no difference).  
Now we have to calculate our *p-value* to compare against out significance level. If p > &alpha;, we accept the null hypothesis that the means are equal. If p ≤ &alpha;, we reject the null hypothesis.  
I could use the SciPy implementation of the Student's t-test to calculate the p-value (not only because it is faster but also less prone to bugs), but for practice purposes I will implement the function myself (and compare to Scipy just to make sure I didn't anything wrong).  
First thing we convert our "FR" (final result) column in the dataframe to two arrays, one for the home wins and the other for away wins. For the home wins we map the "H" to 1 and all the remaining values to 0, while for the away wins the "A" will become 1 and the remaining 0. We also set our &alpha; value.  
```
home_win = np.array(match_data['FR'].replace(to_replace=['H', 'A', 'D'], value=[1, 0, 0], inplace=False))
away_win = np.array(match_data['FR'].replace(to_replace=['H', 'A', 'D'], value=[0, 1, 1], inplace=False))
alpha = 0.05
```  
The function to calculate the p-value is implemented below (it not only return the p-value but also the t-statistic, critical value and degrees of freedom in case someone wants to use instead or together with the p-value).   
```
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
```  
By using this function we get the following results:
```
t_stat, d_f, cv, p = independent_ttest(home_win, away_win, alpha)
t_stat = 1.5635639122196985
d_f = 758
cv = 1.6468663505374166
p = 0.11833738732512233
```  
Just to make sure that the implementation is correct, we compare against SciPy implementation:  
```
t_stat, p = ttest_ind(home_win, away_win)
t_stat = 1.563563912219699
p = 0.11833738732512232
```  
Yes! Our p-value is the same, so the implementation is correct. Now the only thing left is to compare the p-value against &alpha; to check our hypothesis.  
```
p > &alpha; #0.11833738732512232 > 0.05
True
```  
As we can see, our p-value is higher than &alpha;, so that means that we cannot reject the null hypothesis. Therefore, **at the 95% confidence level, there is NO statisticaly difference between the average win-rate of the home teams against the away teams for the 2019-2020 season.**  
Wait!? How can that be possible!? We said at the beggining that home-teams have an advantage against away-teams, why the statistical test says that there is no statisticaly difference between the two?  
Well, we believe that there is a simple answer to that, amount of data. We analyzed only one season (380 matches), and that number is not enough to notice a difference between home and away win, that 21 more wins is not big enough. If we add together other seasons, that difference will be bigger, and if we redo the Student's t-test maybe we will notice a difference in favour of the home teams (will do that when I upload previous seasons data).  
In conclusion: By analyzing one season only, more specifically 2019-2020 season, we can't say that home teams has more chances to win match than the away team.  

### 1.1 - Individual teams home-away advantage  
That is the result by checking all matches, but how about individual teams? We will apply the same statistical analysis to every team to check who performed better at home and who performed better playing away. Before we ignored the matches who ended up on a draw, but here we won't do that, to check for home advantage we will compare the number of home wins against the number of non home wins (away wins + draw). To check for teams who played better away, we do the same, number of away wins against number of non away wins (home wins + draw). Even though, draw a match in soccer is better than losing it, we are giving the same *weight* to both, we are trying to measure if a team wins more when playing at home or away, so even though a drawing is better than losing, it is still a failure to win a match. (code for this analysis is on the italia_statistical_analysis.py)  
#### <img src="/imgs/clubs logo/atalanta.png" width="40">Atalanta  
Home wins: 12/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Atalanta playing at home for the 2019-2020 season.**  
Away wins: 11/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Atalanta playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/bologna.png" width="40">Bologna  
Home wins: 5/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Bologna playing at home for the 2019-2020 season.**  
Away wins: 7/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Bologna playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/brescia.png" width="40">Brescia  
Home wins: 3/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Brescia playing at home for the 2019-2020 season.**  
Away wins: 3/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Brescia playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/cagliari.png" width="40">Cagliari  
Home wins: 7/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Cagliari playing at home for the 2019-2020 season.**  
Away wins: 4/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Cagliari playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/fiorentina.png" width="40">Fiorentina  
Home wins: 5/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Fiorentina playing at home for the 2019-2020 season.**  
Away wins: 7/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Fiorentina playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/genoa.png" width="40">Genoa  
Home wins: 7/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Genoa playing at home for the 2019-2020 season.**  
Away wins: 3/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Genoa playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/hellas verona.png" width="40">Hellas Verona  
Home wins: 9/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Hellas Verona playing at home for the 2019-2020 season.**  
Away wins: 3/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Hellas Verona playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/inter.png" width="40">Inter  
Home wins: 11/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Inter playing at home for the 2019-2020 season.**  
Away wins: 13/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Inter playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/juventus.png" width="40">Juventus  
Home wins: 16/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Juventus playing at home for the 2019-2020 season.**  
Away wins: 10/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Juventus playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/lazio.png" width="40">Lazio  
Home wins: 14/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Lazio playing at home for the 2019-2020 season.**  
Away wins: 10/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Lazio playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/lecce.png" width="40">Lecce  
Home wins: 4/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Lecce playing at home for the 2019-2020 season.**  
Away wins: 5/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Lecce playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/milan.png" width="40">Milan  
Home wins: 9/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Milan playing at home for the 2019-2020 season.**  
Away wins: 10/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Milan playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/napoli.png" width="40">Napoli  
Home wins: 10/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Napoli playing at home for the 2019-2020 season.**  
Away wins: 8/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Napoli playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/parma.png" width="40">Parma  
Home wins: 7/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Parma playing at home for the 2019-2020 season.**  
Away wins: 7/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Parma playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/roma.png" width="40">Roma  
Home wins: 10/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Roma playing at home for the 2019-2020 season.**  
Away wins: 11/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Roma playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/sampdoria.png" width="40">Sampdoria  
Home wins: 6/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Sampdoria playing at home for the 2019-2020 season.**  
Away wins: 6/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Sampdoria playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/sassuolo.png" width="40">Sassuolo  
Home wins: 8/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Sassuolo playing at home for the 2019-2020 season.**  
Away wins: 6/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Sassuolo playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/spal.png" width="40">SPAL  
Home wins: 2/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of SPAL playing at home for the 2019-2020 season.**  
Away wins: 3/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of SPAL playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/torino.png" width="40">Torino  
Home wins: 7/19  
**At the 95% confidence level, there is NO statisticaly difference between the average win-rate of Torino playing at home for the 2019-2020 season.**  
Away wins: 4/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Torino playing away for the 2019-2020 season.**  

#### <img src="/imgs/clubs logo/udinese.png" width="40">Udinese  
Home wins: 6/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Udinese playing at home for the 2019-2020 season.**  
Away wins: 6/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Udinese playing away for the 2019-2020 season.**  

We summarize the result in the following table:  
| | **Home** | **Away** |
| --- | --- | --- |
| **Above average** | <img src="/imgs/clubs logo/juventus.png" width="30"><img src="/imgs/clubs logo/lazio.png" width="30"> | <img src="/imgs/clubs logo/inter.png" width="30"> |
| **Below average** | <img src="/imgs/clubs logo/bologna.png" width="30"><img src="/imgs/clubs logo/brescia.png" width="30"><img src="/imgs/clubs logo/fiorentina.png" width="30"><img src="/imgs/clubs logo/lecce.png" width="30"><img src="/imgs/clubs logo/sampdoria.png" width="30"><img src="/imgs/clubs logo/spal.png" width="30"><img src="/imgs/clubs logo/udinese.png" width="30"> | <img src="/imgs/clubs logo/brescia.png" width="30"><img src="/imgs/clubs logo/cagliari.png" width="30"><img src="/imgs/clubs logo/genoa.png" width="30"><img src="/imgs/clubs logo/hellas verona.png" width="30"><img src="/imgs/clubs logo/lecce.png" width="30"><img src="/imgs/clubs logo/sampdoria.png" width="30"><img src="/imgs/clubs logo/sassuolo.png" width="30"><img src="/imgs/clubs logo/spal.png" width="30"><img src="/imgs/clubs logo/torino.png" width="30"><img src="/imgs/clubs logo/udinese.png" width="30"> |  

As we can see from the table, Juventus and Lazio were the only teams who statisticaly achieved an above average win-rate when playing at home, while Inter was the only club who performed better when playing away. In the bottom row we can check the teams who performed below average at home or away (with a good number of these teams achieving below average on both).


## 2 - Does penalties matter?  
Penalties, the most controversial topic in the world of soccer. After the weekend round, penalties are normally the most discussed topic in TV sports programs or between a group of friends. "It was clearly a foul" or "The player faked, the other guy didn't even touched him", "The foul was outside the penalty area" or "The foul was inside the penalty area", "That handball was clearly a penalty, it would be a goal if wasn't for it" or "That handball was not on purpose, the arm was against his body, he couldn't do anything" and so many statements like this are made to justify or not the award of a penalty. It's understandable why this is a hot topic, compared to other sports like basketball, volleyball and tennis, soccer is a sport where teams score just a few "points" every match (having no "points" scored at all being also common), so having a type of foul that allow a team to score a point easily is a very big deal.  
The introduction of VAR (Video assistent referee) helped a lot in this regard, making it easy for referees, now they don't need to decide a game-changing situation like a penalty in the heat of the moment, they can check many times a replay, check from different angles and then reach a decision (a decision that many fans around the world will still argue against).  
Penalties are important, no doubt about that, it can change the game in just one second. It can bring a team back to life after spending most of the match only defending, it can save the favorite team who spent the whole game "hammering down" the smaller one and didn't got any goal at all. Also have a psychological effect on the players. It's important, but does it affect results in the long run? Dr. Tunde Buraimo [answered this question in the book "Soccernomics"](https://www.goodreads.com/book/show/6617185-soccernomics) by analyzing 1520 Premier League matches, from the 2002/2003 season until the 2005/2006 one. He compared matches where penalties were awarded against the ones where there was no penalty, and checked if there was a difference between the average of home wins, away wins and draws of both groups. In the result, there was an increase of almost 3% of home wins when there was a penalty involved in the match, but at the same time, analysis showed that this difference is not statistically significant. In conclusion, penalties does not change the outcome of matches in the long run.  
That was the result in the long run, but what about one season? One season is not long enough to be considered a long run, so if we analyze it, we may find some differences in the final positions of the clubs at the final table. And that is what we are going to try to answer here, **how much different the Italia Serie A 2019-2020 table would look like if there was no penalties awarded at all?**  

First thing is to check is how many penalties were awarded and in how many games. From the 380 matches of the 2019-2020 season, 147 (38.7%) had at least one penalty awarded against 233 (61.3%) without (chart on the left). In total, 187 penalties were awarded this season, 152 (81.3%) went in while the remaining 35 (18.7%) didn't found the desired target (chart in the middle). From the 1154 goals that happened that season, 152 (13.2%) came from the penalty spot, while the remaining 1002 (86.8%) were by normal play, free kicks and such (chart on the right).  

<img src="/imgs/match_penalty_pie.png" width="380"><img src="/imgs/penalty_accuracy_pie.png" width="260"><img src="/imgs/total_goals_pie.png" width="290">  

Second thing, which team received more penalties, and how many went in. The result is summarized at the table below.  
| | **Team** | **Penalties Awarded** | **Scored** | **Missed** | **%** |
| :---: | :--- | :---: | :---: | :---: | :---: |
| *1* | <img src="/imgs/clubs logo/lazio.png" width="25"> Lazio | 18 | 15 | 3 | 83.3% |
| *2* | <img src="/imgs/clubs logo/genoa.png" width="25"> Genoa | 16 | 11 | 5 | 68.8% |
| *3* | <img src="/imgs/clubs logo/lecce.png" width="25"> Lecce | 15 | 11 | 4 | 73.3% |
| *4* | <img src="/imgs/clubs logo/juventus.png" width="25"> Juventus | 14 | 13 | 1 | 92.9% |
| * | <img src="/imgs/clubs logo/roma.png" width="25"> Roma | 14 | 12 | 2 | 85.7% |
| *6* | <img src="/imgs/clubs logo/sampdoria.png" width="25"> Sampdoria | 12 | 9 | 3 | 75.0% |
| *7* | <img src="/imgs/clubs logo/inter.png" width="25"> Inter | 11 | 10 | 1 | 90.9% |
| * | <img src="/imgs/clubs logo/fiorentina.png" width="25"> Fiorentina | 11 | 9 | 2 | 81.8% |
| *9* | <img src="/imgs/clubs logo/atalanta.png" width="25"> Atalanta | 10 | 7 | 3 | 70.0% |
| *10* | <img src="/imgs/clubs logo/hellas verona.png" width="25"> Hellas Verona | 9 | 8 | 1 | 88.9% |
| * | <img src="/imgs/clubs logo/milan.png" width="25"> Milan | 9 | 8 | 1 | 88.9% |
| *12* | <img src="/imgs/clubs logo/torino.png" width="25"> Torino | 8 | 7 | 1 | 87.5% |
| *13* | <img src="/imgs/clubs logo/spal.png" width="25"> SPAL | 7 | 5 | 2 | 71.4% |
| *14* | <img src="/imgs/clubs logo/bologna.png" width="25"> Bologna | 6 | 5 | 1 | 83.3% |
| * | <img src="/imgs/clubs logo/sassuolo.png" width="25"> Sassuolo | 6 | 5 | 1 | 83.3% |
| * | <img src="/imgs/clubs logo/cagliari.png" width="25"> Cagliari | 6 | 4 | 2 | 66.7% |
| * | <img src="/imgs/clubs logo/parma.png" width="25"> Parma | 6 | 4 | 2 | 66.7% |
| *18* | <img src="/imgs/clubs logo/napoli.png" width="25"> Napoli | 5 | 5 | 0 | 100.0% |
| *19* | <img src="/imgs/clubs logo/brescia.png" width="25"> Brescia | 4 | 4 | 0 | 100.0% |
| *20* | <img src="/imgs/clubs logo/udinese.png" width="25"> Udinese | 0 | -- | -- | ----- |  

As we can see from the table, some teams are awarded more penalties than the others (we will try to answer why in a future analysis), the top place being occupied by Lazio, with the average of almost 1 penalty every two matches, while Udinese wasn't awarded any penalty at all during the 38 matches of the season.  

Now the last and most important one, if we remove these penalties, how much different the table would look like. To do that we subtract every penalty goal from matches and recalculate the number of points obtained. For example, if a match end it up 1x0 with the goal coming from a penalty kick, we will deduce that goal, becoming now 0x0, and recalculate the points. Team 1 will receive 1 instead of 3, while team 2 will receive 1 instead of 0. We do that for every match with at least one pnalty. We show both the original table (on the left) and the modified one (on the right).  

<table>
<tr><th> Original table </th><th> Modified table </th></tr>
<tr><td>

| | **Team** | **P** | **W** | **D** | **L** |
| :---: | :--- | :---: | :---: | :---: | :---: |
| *1* | <img src="/imgs/clubs logo/juventus.png" width="25"> Juventus | 83 | 26 | 5 | 7 |
| *2* | <img src="/imgs/clubs logo/inter.png" width="25"> Inter | 82 | 24 | 10 | 4 |
| *3* | <img src="/imgs/clubs logo/atalanta.png" width="25"> Atalanta | 78 | 23 | 9 | 6 |
| *4* | <img src="/imgs/clubs logo/lazio.png" width="25"> Lazio | 78 | 24 | 6 | 8 |
| *5* | <img src="/imgs/clubs logo/roma.png" width="25"> Roma | 70 | 21 | 7 | 10 |
| *6* | <img src="/imgs/clubs logo/milan.png" width="25"> Milan | 66 | 19 | 9 | 10 |
| *7* | <img src="/imgs/clubs logo/napoli.png" width="25"> Napoli | 62 | 18 | 8 | 12 |
| *8* | <img src="/imgs/clubs logo/sassuolo.png" width="25"> Sassuolo | 51 | 14 | 9 | 15 |
| *9* | <img src="/imgs/clubs logo/hellas verona.png" width="25"> Hellas Verona | 49 | 12 | 13 | 13 |
| *10* | <img src="/imgs/clubs logo/fiorentina.png" width="25"> Fiorentina | 49 | 12 | 13 | 13 |
| *11* | <img src="/imgs/clubs logo/parma.png" width="25"> Parma | 49 | 14 | 7 | 17 |
| *12* | <img src="/imgs/clubs logo/bologna.png" width="25"> Bologna | 47 | 12 | 11 | 15 |
| *13* | <img src="/imgs/clubs logo/udinese.png" width="25"> Udinese | 45 | 12 | 9 | 17 |
| *14* | <img src="/imgs/clubs logo/cagliari.png" width="25"> Cagliari | 45 | 11 | 12 | 15 |
| *15* | <img src="/imgs/clubs logo/sampdoria.png" width="25"> Sampdoria | 42 | 12 | 6 | 20 |
| *16* | <img src="/imgs/clubs logo/torino.png" width="25"> Torino | 40 | 11 | 7 | 20 |
| *17* | <img src="/imgs/clubs logo/genoa.png" width="25"> Genoa | 39 | 10 | 9 | 19 |
| *18* | <img src="/imgs/clubs logo/lecce.png" width="25"> Lecce | 35 | 9 | 8 | 21 |
| *19* | <img src="/imgs/clubs logo/brescia.png" width="25"> Brescia | 25 | 6 | 7 | 25 |
| *20* | <img src="/imgs/clubs logo/spal.png" width="25"> SPAL | 20 | 5 | 5 | 28 |

</td><td>

| | **Team** | **P** | **W** | **D** | **L** | **P diff** | **Pos diff** | **Diff outcome** |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| *1* | <img src="/imgs/clubs logo/atalanta.png" width="25"> Atalanta | 80 | 24 | 8 | 6 | +2 | +2 | 5 |
| *2* | <img src="/imgs/clubs logo/juventus.png" width="25"> Juventus | 78 | 24 | 6 | 8 | -5 | -1 | 5 |
| *3* | <img src="/imgs/clubs logo/inter.png" width="25"> Inter | 75 | 21 | 12 | 5 | -7 | -1 | 5 |
| *4* | <img src="/imgs/clubs logo/lazio.png" width="25"> Lazio | 73 | 22 | 7 | 9 | -5 | -- | 5 |
| *5* | <img src="/imgs/clubs logo/roma.png" width="25"> Roma | 66 | 20 | 6 | 12 | -4 | -- | 8 |
| *6* | <img src="/imgs/clubs logo/napoli.png" width="25"> Napoli | 64 | 18 | 10 | 10 | +2 | +1 | 4 |
| *7* | <img src="/imgs/clubs logo/milan.png" width="25"> Milan | 63 | 18 | 9 | 11 | -3 | -1 | 4 |
| *8* | <img src="/imgs/clubs logo/sassuolo.png" width="25"> Sassuolo | 55 | 15 | 10 | 13 | +4 | -- | 4 |
| *9* | <img src="/imgs/clubs logo/fiorentina.png" width="25"> Fiorentina | 52 | 13 | 13 | 12 | +3 | +1 | 5 |
| *10* | <img src="/imgs/clubs logo/parma.png" width="25"> Parma | 50 | 13 | 11 | 14 | +1 | +1 | 4 |
| *11* | <img src="/imgs/clubs logo/hellas verona.png" width="25"> Hellas Verona | 48 | 10 | 18 | 10 | -1 | -2 | 11 |
| *12* | <img src="/imgs/clubs logo/udinese.png" width="25"> Udinese | 47 | 12 | 11 | 15 | +2 | +1 | 2 |
| *13* | <img src="/imgs/clubs logo/cagliari.png" width="25"> Cagliari | 46 | 11 | 13 | 14 | +1 | +1 | 5 |
| *14* | <img src="/imgs/clubs logo/torino.png" width="25"> Torino | 45 | 13 | 6 | 21 | +5 | +2 | 3 |
| *15* | <img src="/imgs/clubs logo/bologna.png" width="25"> Bologna | 45 | 11 | 12 | 15 | -2 | -3 | 3 |
| *16* | <img src="/imgs/clubs logo/sampdoria.png" width="25"> Sampdoria | 40 | 10 | 10 | 18 | -2 | -1 | 6 |
| *17* | <img src="/imgs/clubs logo/genoa.png" width="25"> Genoa | 36 | 9 | 9 | 20 | -3 | -- | 10 |
| *18* | <img src="/imgs/clubs logo/lecce.png" width="25"> Lecce | 32 | 7 | 11 | 20 | -3 | -- | 5 |
| *19* | <img src="/imgs/clubs logo/brescia.png" width="25"> Brescia | 27 | 7 | 6 | 25 | +2 | -- | 7 |
| *20* | <img src="/imgs/clubs logo/spal.png" width="25"> SPAL | 20 | 4 | 8 | 26 | -- | -- | 5 |

</td></tr> </table>  

From the 147 matches with a least one penalty, 53 would change the final outcome if we deduct the goal(s) from the penalty spot. The first thing to notice in the modified league table is the new champion. Thanks to the 2 extra points, Atalanta would rise to the top, while Juventus and Inter would drop off one position each thanks to the loss of 5 and 7 points respectively. But besides that, there is not much else to notice in the table, mostly teams would drop/go up just one position while the bottom part would remain unchanged. Another thing to notice is the last column, how many matches would have a different outcome for each team. The average of all is around 5 each, with Udinese only having 2 while for Hellas Verona 11 matches would have end it up differently. Even though many matches would have a different outcome, the points difference is not that big, with a average of ±3 points for each team, meaning just one more/less win.  

Going back to the title of this section "does penalties matter?". Well, in that case the answer will depends on who you ask, some people will say "of course, it would have a different champion, that changes everything", while others will say "it does not matter much, many teams would have the same final place and the number of points obtained for each wouldn't be that much different also". So in the end, the answer for this question is just like penalties, controversial.


#### Notes ####
All the data was obtained by using a python script on the official match reports available at the "Lega Serie A" official website.  
The ball possesion data is scouted live through the television, with an estimate error of 5%.  

If you spot a mistake, please don't hesitate to open an issue or contact me at evaldo.lborba(at)gmail.com