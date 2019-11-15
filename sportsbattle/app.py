# import the Flask class fromt he flask mod
from flask import Flask, render_template, redirect, session, url_for, request, flash
#import pymsgbox
from functools import wraps

userpass = {'admin': 'admin'}
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
            return redirect(url_for('home'))
        else:
            error = "User already exists."
            flash(error)
    return render_template('splash.html', error=error)

@app.route('/home')
@login_required
def home():
    return render_template('main.html')

'''
@app.route('/welcome')
def welcome():
	return "Hello world!"
'''  

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in userpass.keys() or request.form['password'] not in userpass.values():
            error = "Invalid Creds, try again."
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('splash'))


if __name__ == '__main__':
    app.run(debug=True)
