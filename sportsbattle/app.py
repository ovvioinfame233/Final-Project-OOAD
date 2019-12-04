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
            
            ### we want create the user file and append the username.
            
            return redirect(url_for('home'))
        else:
            error = "User already exists."
            flash(error)
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
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))

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
    infile = open('leagueNames.csv', 'r')
    for row in infile:
        info = row.split(',')
        leaguenames[info[0]] = info[1]
    app.run(debug=True)
