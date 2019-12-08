# import the Flask class fromt he flask mod
from flask import Flask, render_template, redirect, session, url_for, request, flash
#import pymsgbox
from functools import wraps
import csv
from sportsreference.nfl.boxscore import Boxscores
import os
from pathlib import Path
from string import Template



### probaly in the main 
## as soon as the app starts
## read all the user files
## append to userpass

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


#userpass = {'admin': 'admin'}
#leaguenames = {'admin':'admin'}
#currentuser = ""
currentuser = None
#usersLeauges = []
# Create the app object
app = Flask(__name__)
app.debug = True
app.secret_key = 'hello'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


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
@app.route('/signup', methods=['GET', 'POST'])
def splash():
    error = None
    success = "You are now signed up"
    if request.method == 'POST':
        found = False
        for person in Users:
            if (person.username == request.form['username']):
                found = True
                error = "User already exists."
                return render_template('splash.html', error=error)
        if found == False:            
            global currentuser
            #userpass[request.form['username']] = request.form['password']
            newUser = User(request.form['username'],request.form['password'])
            session['logged_in'] = True
            userfile = open('users/%s.csv' % request.form['username'], 'w+')
            with open('userNames.csv', 'a') as names:
                names.write(request.form['username']+','+request.form['password']+"\n")
            currentuser = newUser
            Users.append(newUser)
            return redirect(url_for('home'))
    return render_template('splash.html', error=error)
    

@app.route('/home')
@login_required

def home():
    return render_template('main.html',usersLeauges = currentuser.usersCurrentLeauges)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        
        # if request.form['username'] not in userpass.keys() or request.form['password'] not in userpass.values():
        #     error = "Invalid Creds, try again."
        found = False
        for person in Users:
            if(person.username == request.form['username'] and person.password == request.form['password'] ):
                found = True
                global currentuser
                currentuser = person
                session['logged_in'] = True
                full_path = os.path.realpath(__file__)
                directory = os.path.dirname(full_path)+"/Users"
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
    # Prints a dictionary of all matchups for week 1 of 2017
    
    #games_today.game
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
        
    if request.method == 'POST':
        pickspath = Path('picks/%s.csv' % team)
        if not pickspath.is_file():
            error = "You have already made picks for this week"
        else:
            with open('picks/%s.csv' % team, 'a') as picksOut:
                picksOut.write(currentuser.Name + ',')
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
            elif len(currentuser.usersCurrentLeauges) >= 3:
                error = "You can only be in 3 Leauges at once"
            else:
                #leaguenames[request.form['leagueName']] = request.form['leagueCode']
                newLeg = Leg(request.form['leagueName'],request.form['leagueCode'])
                with open('leagueNames.csv', 'a') as outfile:
                    outfile.writelines(request.form['leagueName']+','+request.form['leagueCode']+"\n")
                with open('leagues/%s.csv' % request.form['leagueName'], 'a') as leagueOutfile:
                    # fieldnames = ['username', 'score']
                    # writer = csv.DictWriter(leagueOutfile, fieldnames=fieldnames)
                    # writer.writerow({'username' : currentuser, 'score' : 0 })
                    leagueOutfile.write(currentuser.username+','+'0'+'\n')
                with open('users/%s.csv' % currentuser.username, 'a') as out:
                    # fieldnames = ['league', 'score']
                    # writer = csv.DictWriter(out, fieldnames=fieldnames)
                    # writer.writerow({'league' : request.form['leagueName'], 'score' : 0})
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
        if len(currentuser.usersCurrentLeauges) >= 3:
            error = "You can only be in 3 Leauges at once"
            return render_template('joinleague.html', error=error)
        for legCheck in Legs:
            if request.form['leagueCode'] == legCheck.Code:
                found = True
                with open('leagues/%s.csv' % legCheck.name , 'a') as leagueOutfile:
                    # fieldnames = ['username', 'score']
                    # writer = csv.DictWriter(leagueOutfile, fieldnames=fieldnames)
                    # writer.writerow({'username' : currentuser, 'score' : 0 })
                    leagueOutfile.write(currentuser.username+','+'0'+'\n')
                with open('users/%s.csv' % currentuser.username, 'a') as out:
                    # fieldnames = ['league', 'score']
                    # writer = csv.DictWriter(out, fieldnames=fieldnames)
                    # writer.writerow({'league' : key, 'score' : 0})
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

@app.route('/teamOne',methods = ['POST', 'GET'])
@login_required
def teamOne():
    # Prints a dictionary of all matchups for week 1 of 2017 
    Pokemons =["Pikachu", "Charizard", "Squirtle", "Jigglypuff", "Bulbasaur", "Gengar", "Charmander", "Mew", "Lugia", "Gyarados"] 
    lens = len(Pokemons)
    games_today = Boxscores(9, 2019)
    # Prints a dictionary of all matchups for week 1 of 2017
    #print(games_today.games)
    #games_today.game
    stef = games_today._boxscores
    week = "9"
    year = "2019"
    numberOfGames = len(stef[week+'-'+year])
    winners = []
    for i in range(numberOfGames):
        f = stef['9-2019'][i]['winning_name']
        winners.append(f)
    lens = len(winners)
    return render_template('teamOne.html',lens = lens,winners = winners, usersLeauges = currentuser.usersCurrentLeauges )

@app.route('/teamTwo', methods=['POST', 'GET'])
@login_required
def teamTwo():
    global currentuser
    error = None
    gamesThisWeek = Boxscores(9, 2019)
    # Prints a dictionary of all matchups for week 1 of 2017
    
    #games_today.game
    Libary = gamesThisWeek._boxscores
    week = "9"
    year = "2019"
    numberOfGames = len(Libary[week+'-'+year])
    games = []

    for i in range(numberOfGames):
        home = Libary['9-2019'][i]['home_name']
        away = Libary['9-2019'][i]['away_name']
        hmm = { 'Home':home,
                'Away' : away
            }
        games.append(hmm)
        
    if request.method == 'POST':
        pickspath = Path('picks/%s.csv' % currentuser)
        if pickspath.is_file():
            error = "You have already made picks for this week"
        else:
            with open('picks/%s.csv' % currentuser, 'a') as picksOut:
                picksOut.write(currentuser + ',')
                for x in range(1,15):
                    picksOut.write(request.form['row-%s' % str(x)] + ',')
            return redirect(url_for('home'))
    return render_template('teamTwo.html',games = games, error=error, usersLeauges = currentuser.usersCurrentLeauges )



@app.route('/teamThree')
@login_required
def teamThree():
    full_path = os.path.realpath(__file__)
    directory = os.path.dirname(full_path)+"/leagues"
    Leaders = []
    with open(directory+'/league1.csv', 'r') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            NameScore = {'Name': row[0],
                         'Score' : int(row[1])    
                    }
            Leaders.append(NameScore)
    Leaders = sorted(Leaders, key = lambda i: i['Score'],reverse=True) 
    return render_template('teamThree.html',Leaders = Leaders, usersLeauges = currentuser.usersCurrentLeauges )


if __name__ == '__main__':
    
    infileleagues = open('leagueNames.csv', 'r')
    for row in infileleagues:
        info = row.split(',')
        info[1] = info[1].strip('\n')
        #leaguenames[info[0]] = info[1]
        newLeg = Leg(info[0],info[1])
        Legs.append(newLeg)
    infileusers = open('userNames.csv', 'r')
    for row2 in infileusers:
        info2 = row2.split(',')
        info2[1] = info2[1].strip('\n')
        #userpass[info2[0]] = info2[1]
        newUser = User(info2[0],info2[1])
        Users.append(newUser)
    ##This is where we're going to need to add the capability to read the games that week
    ##This is also probably where we're going to put all our data for the games and stuff
    app.run(use_reloader = True,debug=True)
