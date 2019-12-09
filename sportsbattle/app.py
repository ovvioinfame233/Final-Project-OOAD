# import the Flask class fromt he flask mod
from flask import Flask, render_template, redirect, session, url_for, request, flash
#import pymsgbox
from functools import wraps
import csv
from sportsreference.nfl.boxscore import Boxscores
import os
from pathlib import Path
from string import Template

## user class fro each user
class User:
    usersCurrentLeauges = ["","",""]
    def __init__(self, username, password):
        self.username = username
        self.password = password
#holds all users will be filled in the main
Users= []

#holds all legauges will be filled in the main
Legs = []
#Thi is the Leauges object 
class Leg:
    def __init__(self, Name, Code):
        self.name = Name
        self.Code = Code
# This will hold the current user object
currentuser = None
# Create the app object
app = Flask(__name__)
app.debug = True
app.secret_key = 'hello'
## this is to prevent caches from breaking stuff
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

## a user trying to get to a page they arent allowed to use
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# Decorators to link function to a URL
## This is the sign up page 
@app.route('/signup', methods=['GET', 'POST'])
def splash():
    error = None 
    success = "You are now signed up"
    if request.method == 'POST':
        found = False
        for person in Users:
            ## if that user name is already taken
            if (person.username == request.form['username']):
                found = True
                error = "User already exists."
                return render_template('splash.html', error=error)
        ## Otherwise create the user 
        if found == False:            
            global currentuser
            newUser = User(request.form['username'],request.form['password'])
            session['logged_in'] = True
            ## create file with username and password
            userfile = open('users/%s.csv' % request.form['username'], 'w+')
            with open('userNames.csv', 'a') as names:
                names.write(request.form['username']+','+request.form['password']+"\n")
            ## set current user
            currentuser = newUser
            Users.append(newUser)
            ## go to home page
            return redirect(url_for('home'))
    return render_template('splash.html', error=error)
    

@app.route('/home')
@login_required
## sends the leauges the user is in to the front page
def home():
    return render_template('main.html',usersLeauges = currentuser.usersCurrentLeauges)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        found = False
        for person in Users:
            ## if username and passwords mathches
            if(person.username == request.form['username'] and person.password == request.form['password'] ):
                found = True
                global currentuser
                currentuser = person
                session['logged_in'] = True
                full_path = os.path.realpath(__file__)
                directory = os.path.dirname(full_path)+"/Users"
                ## here we will read in the leagues the user is in.
                with open(directory+"/"+currentuser.username+".csv", 'r') as csv_file:
                    count = 0
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        if(row != [] ):
                            for legCheck in Legs:
                                if(legCheck.name == row[0]):
                                    if currentuser.usersCurrentLeauges[0] == "":
                                        currentuser.usersCurrentLeauges[0] = legCheck.name
                                    elif currentuser.usersCurrentLeauges[1] == "":
                                        currentuser.usersCurrentLeauges[1] = (legCheck.name)
                                    elif currentuser.usersCurrentLeauges[2] == "":
                                        currentuser.usersCurrentLeauges[2] = (legCheck.name)
                return redirect(url_for('home'))
        if ( found == False):
            error = "User or Password not found."
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    global currentuser
    currentuser = None
    return redirect(url_for('login'))

@app.route('/makepicks/<team>', methods=['POST', 'GET'])
@login_required
def makepicks(team):
    global currentuser
    error = None
    gamesThisWeek = Boxscores(9, 2019)    
    Libary = gamesThisWeek._boxscores
    week = "9"
    year = "2019"
    numberOfGames = len(Libary[week+'-'+year])
    games = []
    global currentuser
    for i in range(numberOfGames):
        home = Libary['9-2019'][i]['home_name']
        away = Libary['9-2019'][i]['away_name']
        hmm = { 'Home':home,
                'Away' : away
            }
        games.append(hmm)
    alreadyPicked = []
    full_path = os.path.realpath(__file__)
    if request.method == 'POST':
        directory = os.path.dirname(full_path)+"/picks"
        PicksFile = open(directory+"/"+team+".csv", 'a+')
        for row2 in PicksFile:
            info = row2.split(',')
            WhoPicked = info[0]
            alreadyPicked.append(WhoPicked)
        if currentuser.username in alreadyPicked:
            error = "You have already made your picks this week"
            return render_template('makepicks.html',error = error)
        else:
            with open('picks/%s.csv' % team, 'a+') as picksOut:
                picksOut.write(currentuser.username + ',')
                for x in range(1,15):
                    picksOut.write(request.form['row-%s' % str(x)] + ',')
            return redirect(url_for('home'))

    return render_template('makepicks.html',games = games, error=error, usersLeauges = currentuser.usersCurrentLeauges, team=team)

@app.route('/createleague', methods=['GET', 'POST'])
@login_required
def createleague():
    error = None
    if request.method == 'POST':
        for LegCheck in Legs:
            if request.form['leagueName'] == LegCheck.name:
                error = "Leauge Name Taken"
            elif currentuser.usersCurrentLeauges[0] != "" and currentuser.usersCurrentLeauges[1] != "" and currentuser.usersCurrentLeauges[3] != "":
                error = "You can only be in 3 Leauges at once"
            else:
                newLeg = Leg(request.form['leagueName'],request.form['leagueCode'])
                ## appending to the leaguenames file
                with open('leagueNames.csv', 'a') as outfile:
                    outfile.writelines(request.form['leagueName']+','+request.form['leagueCode']+"\n")
                ## creating the league file
                with open('leagues/%s.csv' % request.form['leagueName'], 'a') as leagueOutfile:
                    leagueOutfile.write(currentuser.username+','+'0'+'\n')
                ## adding league to users file
                with open('users/%s.csv' % currentuser.username, 'a') as out:
                    out.write(request.form['leagueName']+','+'0'+'\n')
                    if currentuser.usersCurrentLeauges[0] == "":
                        currentuser.usersCurrentLeauges[0]=(newLeg.name)
                    elif currentuser.usersCurrentLeauges[1] == "":
                        currentuser.usersCurrentLeauges[1]=(newLeg.name)
                    elif currentuser.usersCurrentLeauges[2] == "":
                        currentuser.usersCurrentLeauges[2]=(newLeg).name
                Legs.append(newLeg)
                return redirect(url_for('home'))

    return render_template('createleague.html', error=error)

@app.route('/joinleague', methods=['GET', 'POST'])
@login_required
def joinleague():
    error = None
    if request.method == 'POST':
        found = False
        if currentuser.usersCurrentLeauges[0] != "" and currentuser.usersCurrentLeauges[1] != "" and currentuser.usersCurrentLeauges[3] != "":
            error = "You can only be in 3 Leauges at once"
            return render_template('joinleague.html', error=error)
        for legCheck in Legs:
            ## adding league to users file and league file
            if request.form['leagueCode'] == legCheck.Code:
                found = True
                with open('leagues/%s.csv' % legCheck.name , 'a') as leagueOutfile:
                    leagueOutfile.write(currentuser.username+','+'0'+'\n')
                with open('users/%s.csv' % currentuser.username, 'a') as out:
                    out.write( legCheck.name+','+'0'+'\n')
                    if currentuser.usersCurrentLeauges[0] == "":
                        currentuser.usersCurrentLeauges[0]=(legCheck.name)
                    elif currentuser.usersCurrentLeauges[1] == "":
                        currentuser.usersCurrentLeauges[1]=(legCheck.name)
                    elif currentuser.usersCurrentLeauges[2] == "":
                        currentuser.usersCurrentLeauges[2]=(legCheck.name)
                return redirect(url_for('home'))
        if found == False:
            error = "Incorrect League Code"
    return render_template('joinleague.html', error=error)

## will be the league scoreboard
@app.route('/teamOne',methods = ['POST', 'GET'])
@login_required
def teamOne():
    full_path = os.path.realpath(__file__)
    directory = os.path.dirname(full_path)+"/leagues"
    Leaders = []
    with open(directory+'/%s.csv' % currentuser.usersCurrentLeauges[0], 'r') as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            NameScore = {'Name': row[0],
                         'Score' : int(row[1])    
                    }
            Leaders.append(NameScore)
    Leaders = sorted(Leaders, key = lambda i: i['Score'],reverse=True) 
    print(Leaders)
    return render_template('teamOne.html',Leaders = Leaders, usersLeauges = currentuser.usersCurrentLeauges )
## will be the league scoreboard
@app.route('/teamTwo', methods=['POST', 'GET'])
@login_required
def teamTwo():
    full_path = os.path.realpath(__file__)
    directory = os.path.dirname(full_path)+"/leagues"
    Leaders = []
    with open(directory+'/%s.csv' % currentuser.usersCurrentLeauges[1], 'r') as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            NameScore = {'Name': row[0],
                         'Score' : int(row[1])    
                    }
            Leaders.append(NameScore)
    Leaders = sorted(Leaders, key = lambda i: i['Score'],reverse=True) 
    print(Leaders)
    return render_template('teamTwo.html',Leaders = Leaders, usersLeauges = currentuser.usersCurrentLeauges )
## will be the league scoreboard
@app.route('/teamThree')
@login_required
def teamThree():
    full_path = os.path.realpath(__file__)
    directory = os.path.dirname(full_path)+"/leagues"
    Leaders = []
    with open(directory+'/%s.csv' % currentuser.usersCurrentLeauges[2], 'r') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            NameScore = {'Name': row[0],
                         'Score' : int(row[1])    
                    }
            Leaders.append(NameScore)
    Leaders = sorted(Leaders, key = lambda i: i['Score'],reverse=True) 
    
    return render_template('teamThree.html',Leaders = Leaders, usersLeauges = currentuser.usersCurrentLeauges )

## shows who won the games last week.
@app.route('/lastweek')
@login_required
def lastweek():
    games_today = Boxscores(9, 2019)
    stef = games_today._boxscores
    week = "9"
    year = "2019"
    numberOfGames = len(stef[week+'-'+year])
    winners = []
    for i in range(numberOfGames):
        f = stef['9-2019'][i]['winning_name']
        winners.append(f)
    lens = len(winners)
    return render_template('lastweek.html',lens = lens,winners = winners, usersLeauges = currentuser.usersCurrentLeauges )


if __name__ == '__main__':
    ## reading in all of the leagues
    infileleagues = open('leagueNames.csv', 'r')
    for row in infileleagues:
        info = row.split(',')
        info[1] = info[1].strip('\n')
        newLeg = Leg(info[0],info[1])
        Legs.append(newLeg)
    ## reading in all the users
    infileusers = open('userNames.csv', 'r')
    for row2 in infileusers:
        info2 = row2.split(',')
        info2[1] = info2[1].strip('\n')
        newUser = User(info2[0],info2[1])
        Users.append(newUser)
    app.run(use_reloader = True,debug=True)
