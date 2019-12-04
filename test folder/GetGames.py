class Game:
    def __init__(self, home, away):
        self.home = home
        self.away = away

from sportsreference.nfl.boxscore import Boxscores
games_today = Boxscores(9, 2019)
# Prints a dictionary of all matchups for week 1 of 2017
print(games_today.games)
#games_today.game
stef = games_today._boxscores
week = "9"
year = "2019"
numberOfGames = len(stef[week+'-'+year])
games = []
for i in range(numberOfGames):
    home = stef['9-2019'][i]['home_name']
    away = stef['9-2019'][i]['away_name']
    game = Game(home,away)
    games.append(game)


tester = 5