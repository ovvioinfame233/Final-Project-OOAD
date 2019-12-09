import os
import csv
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

infileusers = open('userNames.csv', 'r')
for row2 in infileusers:
    info2 = row2.split(',')
    info2[1] = info2[1].strip('\n')
    #userpass[info2[0]] = info2[1]
    newUser = User(info2[0],info2[1])
    Users.append(newUser)

found = False
infileleagues = open('leagueNames.csv', 'r')
for row in infileleagues:
    info = row.split(',')
    info[1] = info[1].strip('\n')
    #leaguenames[info[0]] = info[1]
    newLeg = Leg(info[0],info[1])
    Legs.append(newLeg)

    
found = True

newcurrentuser = Users[0]

# full_path = os.path.realpath(__file__)
# directory = os.path.dirname(full_path)+"/picks"
# with open(directory+"/"+newcurrentuser.username+".csv", 'r') as csv_file:
    # count = 0
    # csv_reader = csv.reader(csv_file, delimiter=',')
    # for row in csv_reader:
    #     if(row != [] ):
    #         for legCheck in Legs:
    #             if(legCheck.name == row[0]):
    #                 if newcurrentuser.usersCurrentLeauges[0] == "":
    #                     newcurrentuser.usersCurrentLeauges[0] = legCheck
    #                 elif newcurrentuser.usersCurrentLeauges[1] == "":
    #                     newcurrentuser.usersCurrentLeauges[1] = (legCheck)
    #                 elif newcurrentuser.usersCurrentLeauges[2] == "":
    #                     newcurrentuser.usersCurrentLeauges[2] = (legCheck)
alreadyPicked = []
# with open('picks/%s.csv' % "test1", 'a') as leagueOutfile:
#     for row2 in leagueOutfile:
#         info = row2.split(',')
#         WhoPicked = info[0]
#         alreadyPicked.append(WhoPicked)


full_path = os.path.realpath(__file__)
directory = os.path.dirname(full_path)+"/picks"
with open(directory+"/"+"test1"+".csv", 'r') as csv_file:
     for row2 in csv_file:
        info = row2.split(',')
        WhoPicked = info[0]
        alreadyPicked.append(WhoPicked)
        



stef = 5
