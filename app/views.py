from app import app
from flask import render_template, request, flash, url_for, redirect
from flask_login import login_user, LoginManager, login_required
from .database import *
from .UserLogin import UserLogin


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().get_user(user_id)


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/register', methods=['get', 'post'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    error = False
    username = request.values.get('username').lower()
    email = request.values.get('email').lower()
    password = request.values.get('password')
    password_repeat = request.values.get('password_repeat')

    if password != password_repeat:
        error = True
        flash('Passwords must be same')

    if len(password) < 8:
        error = True
        flash('Password must be more than 8 symbols')

    if user_exists(email):
        error = True
        flash('User with this email already exists')

    if error:
        return render_template('register.html')
    else:
        create_user(username, password, email)
        flash('Success')

    return render_template('login.html')


@app.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'POST':
        username = request.values.get('username').lower()
        password = request.values.get('password')

        user = get_user_by_login(username)
        password_hash = sha256(password.encode('utf-8')).hexdigest()
        if user and user.password == password_hash:
            user_login = UserLogin().create(user)
            login_user(user_login)
            return render_template('index.html')
        flash('Invalid login or password')

    return render_template('login.html')
