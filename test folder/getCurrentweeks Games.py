from sportsreference.nfl.boxscore import Boxscores

games_today = Boxscores(18, 2018)
# Prints a dictionary of all matchups for week 1 of 2017
print(games_today.games)
#games_today.game
stef = games_today._boxscores
# print(games_today._boxscores['18-2018']['winning_name'])
print(type(stef))
f = stef['18-2018'][0]['winning_name']
print(stef.get(0))
#g = f[0]
#win = g['winning_name']





bad = 6