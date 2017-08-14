from .models import User
from flask import Flask, request, session, redirect, url_for, render_template, flash

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
	return render_template('index.html')
@app.route('/register', methods=['GET','POST'])
def register():
	if request.method=="POST":
		username = request.form['username']
		password = request.form['password']
		if(len(username)<1):
			flash('Username atleast one character')
		elif not User(username).register(password):
			flash('username already exists')
		else:
			session['username'] = username
			flash('Registered. Logged In successfully')
			return redirect(url_for('index'))
	return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not User(username).verify_password(password):
            flash('Invalid login.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))


