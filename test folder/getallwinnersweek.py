from sportsreference.nfl.boxscore import Boxscores

games_today = Boxscores(9, 2019)
# Prints a dictionary of all matchups for week 1 of 2017
print(games_today.games)
#games_today.game
stef = games_today._boxscores
week = "9"
year = "2019"
numberOfGames = len(stef[week+'-'+year])
winners = []
for i in range(numberOfGames):
    f = stef['9-2019'][i]['winning_name']
    winners.append(f)
print(winners)


def WriteGames():
    f = open("StefanoWeek9.txt","a")
    f.writelines("Stefano\n")
    f.writelines("ASDASD\n")

WriteGames()
