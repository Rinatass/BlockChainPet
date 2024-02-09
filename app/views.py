from app import app
from flask import render_template, request, flash, url_for, redirect
from .database import Database
db = Database()

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/register', methods=['get', 'post'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    error = False
    username = request.values.get('username')
    email = request.values.get('email')
    password = request.values.get('password')
    password_repeat = request.values.get('password_repeat')

    if password != password_repeat:
        error = True
        flash('Pwd error')

    if len(password) < 8:
        error = True
        flash('Pwd len error')

    if db.user_exists(email):
        error = True
        flash('Exists')

    if error:
        return redirect(url_for('register'))
    else:
        db.create_user(username, password, email)
        flash('Успешно')

    return render_template('login.html')





@app.route('/login')
def login():
    return render_template('login.html')