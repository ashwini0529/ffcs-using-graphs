from .models import User, fetch_all_courses
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
@app.route('/add/course', methods=['GET', 'POST'])
def store():
	if request.method=="POST":
		course_code=request.form['course_code']
		course_name=request.form['course_name']
		if not course_code:
			flash('You must provide course code')
		elif not course_name:
			flash('You must provide course name')
		else:
			User(session['username']).add_course(course_name, course_code)
		return redirect(url_for('index'))
	return render_template('add_course.html')
@app.route('/add/pre-requisite', methods=['GET','POST'])
def linkCourses():
	if request.method=="POST":
		course_code=request.form['course_code']
		pr_course_code=request.form['pr_course_code']
		if not pr_course_code:
			flash('Please provide Pre requisite Course Code')
		elif not course_code:
			flash('Please provide Course Code')
		else:
			User(session['username']).add_preRequisite(course_code, pr_course_code)
		return redirect(url_for('index'))
	courses = list(fetch_all_courses())
	return render_template('add_prerequisite.html', courses=courses)


