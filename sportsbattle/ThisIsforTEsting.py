import os
import csv

from sportsreference.nfl.boxscore import Boxscores
full_path = os.path.realpath(__file__)
directory = os.path.dirname(full_path)+"/Users"
class User:
    usersCurrentLeauges = ["","",""]
    def __init__(self, username, password):
        self.username = username
        self.password = password
Users= []
Legs = []
class Leg:
    def __init__(self, Name, Code):
        self.name = Name
        self.Code = Code

class PickChecker:
    def __init__(self, username, picks):
        self.username = username
        self.picks = picks

class LeadboardRow:
    def __init__(self, username, score):
        self.username = username
        self.score = score

PickCheckerList = []
full_path = os.path.realpath(__file__)
directory = os.path.dirname(full_path)+"/picks"
ListofPickCheckers = []
with open(directory+'/%s.csv' % "test2", 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        ListOfWinners = []
        if len(row) != 0:
            name = row[0]
            RedoRow = row
            RedoRow.pop(0)
            for item in RedoRow:
                if item != '':
                    ListOfWinners.append(item)
            Done = PickChecker(name,ListOfWinners)
            PickCheckerList.append(Done)

games_today = Boxscores(9, 2019)
stef = games_today._boxscores
week = "9"
year = "2019"
numberOfGames = len(stef[week+'-'+year])
winners = []
ListOfLeadboardRow = []
for i in range(numberOfGames):
    f = stef['9-2019'][i]['winning_name']
    winners.append(f)

directory = os.path.dirname(full_path)+"/leagues"
with open(directory+'/%s.csv' % "test2", 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        row = LeadboardRow(row[0],row[1])
        ListOfLeadboardRow.append(row)

for item in PickCheckerList:
        count = 0
        for WinnerPicked in item.picks:
            if WinnerPicked in winners:
                count = count + 1
        for LeadboardRowCheck in ListOfLeadboardRow:
            if LeadboardRowCheck.username == item.username:
                LeadboardRowCheck.score = int(LeadboardRowCheck.score) + count
directory = os.path.dirname(full_path)+"/leagues"
with open(directory+'/%s.csv' % "test2", 'w') as csv_file:
    for item in ListOfLeadboardRow:
        csv_file.write(str(item.username)+","+str(item.score)+"\n")
directory = os.path.dirname(full_path)+"/picks"
empty = False
with open(directory+'/%s.csv' % "test2", 'r') as csv_file:
    emptycheck = csv_file.read(1)
    if not emptycheck:
        empty = True
if empty == False:
    with open(directory+'/%s.csv' % "test2", 'w+') as csv_file:
        NeedThisForIndent = 5

#ListOfLeadboardRow.sort(key= lambda x: x.score , reverse=True)
stef = 455


games_today = Boxscores(13, 2019)
stef = games_today._boxscores
week = "13"
year = "2019"
numberOfGames = len(stef[week+'-'+year])
winners = []
for i in range(numberOfGames):
    f = stef['13-2019'][i]['winning_name']
    winners.append(f)
lens = len(winners)