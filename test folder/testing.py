from sportsreference.nfl.boxscore import Boxscores

games_today = Boxscores(1, 2019)
# Prints a dictionary of all matchups for week 1 of 2017
print(games_today.games)