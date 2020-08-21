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

#### <img src="/imgs/clubs logo/spal.png" width="40">Spal  
Home wins: 2/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Spal playing at home for the 2019-2020 season.**  
Away wins: 3/19  
**At the 95% confidence level, there is statisticaly difference between the average win-rate of Spal playing away for the 2019-2020 season.**  

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


#### Notes ####
All the data was obtained by using a python script on the official match reports available at the "Lega Serie A" official website.  
The ball possesion data is scouted live through the television, with an estimate error of 5%.  

If you spot a mistake, please don't hesitate to open an issue or contact me at evaldo.lborba(at)gmail.com