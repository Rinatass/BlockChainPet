from flask import render_template, request, flash, url_for, redirect, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from .database import *
from . import celery_tasks

my_app = Blueprint('main', __name__, template_folder='templates')


@my_app.context_processor
def inject_user():
    return dict(user=current_user)


@my_app.route('/')
def index():
    celery_tasks.wait.delay()
    return render_template('index.html', current_user=current_user)


@my_app.route('/register', methods=['get', 'post'])
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


@my_app.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'POST':
        username = request.values.get('username').lower()
        password = request.values.get('password')
        remember_me = request.values.get('checkbox')

        user = get_user_by_login(username)
        password_hash = sha256(password.encode('utf-8')).hexdigest()

        if user and user.password == password_hash:
            login_user(user, remember=remember_me)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid login or password')

    return render_template('login.html')


@my_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')


