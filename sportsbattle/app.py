# import the Flask class fromt he flask mod
from flask import Flask, render_template, redirect, session, url_for, request, flash
#import pymsgbox
from functools import wraps
import csv


### probaly in the main 
## as soon as the app starts
## read all the user files
## append to userpass


userpass = {'admin': 'admin'}
leaguenames = {'admin':'admin'}
currentuser = [None]

# Create the app object
app = Flask(__name__)
app.secret_key = 'hello'



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
@app.route('/', methods=['GET', 'POST'])
def splash():
    error = None
    success = "You are now signed up"
    if request.method == 'POST':
        if request.form['username'] not in userpass.keys():
            userpass[request.form['username']] = request.form['password']
            session['logged_in'] = True
            userfile = open('users/%s.csv' % request.form['username'], 'w+')
            with open('userNames.csv', 'a') as names:
                fieldnames = ['username', 'password']
                writer = csv.DictWriter(names, fieldnames=fieldnames)
                writer.writerow({'username': request.form['username'], 'password' : request.form['password']})
            return redirect(url_for('home'))
        else:
            error = "User already exists."
    return render_template('splash.html', error=error)

@app.route('/home')
@login_required
def home():
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in userpass.keys() or request.form['password'] not in userpass.values():
            error = "Invalid Creds, try again."
        else:
            currentuser[0] = request.form['username']
            session['logged_in'] = True
            
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('splash'))

@app.route('/makepicks')
@login_required
def makepicks():
    return render_template('makepicks.html')

@app.route('/createleague', methods=['GET', 'POST'])
@login_required
def createleague():
    error = None
    if request.method == 'POST':
        if request.form['leagueName'] in leaguenames.keys():
            error = "League Already Exists"
        else:
            leaguenames[request.form['leagueName']] = request.form['leagueCode']
            with open('leagueNames.csv', 'a') as outfile:
                fieldnames = ['leagueName', 'leagueCode']
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writerow({'leagueName' : request.form['leagueName'], 'leagueCode' : request.form['leagueCode']})
            with open('leagues/%s.csv' % request.form['leagueName'], 'a') as leagueOutfile:
                fieldnames = ['username', 'score']
                writer = csv.DictWriter(leagueOutfile, fieldnames=fieldnames)
                writer.writerow({'username' : currentuser[0], 'score' : 0 })
            with open('users/%s.csv', 'a') as out:
                fieldnames = ['league', 'score']
                writer = csv.DictWriter(out, fieldnames=fieldnames)
                writer.writerow({'league' : request.form['leagueName', 'score' : 0]})
            return redirect(url_for('home'))
    return render_template('createleague.html', error=error)

@app.route('/teamOne')
@login_required
def teamOne():
    return render_template('teamOne.html')

@app.route('/teamTwo')
@login_required
def teamTwo():
    return render_template('teamTwo.html')

@app.route('/teamThree')
@login_required
def teamThree():
    return render_template('teamThree.html')


if __name__ == '__main__':
    infileleagues = open('leagueNames.csv', 'r')
    for row in infileleagues:
        info = row.split(',')
        leaguenames[info[0]] = info[1]
    infileusers = open('userNames.csv', 'r')
    for row in infileusers:
        info = row.split(',')
        userpass[info[0]] = info[1]
    app.run(debug=True)
