from flask import render_template, request, flash, url_for, redirect, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from app.database import *
from app.mongo import *
from app.models import Transaction
from app.celery_tasks import process_block
from app.blockchain import count_balance
my_app = Blueprint('main', __name__, template_folder='templates')


# Provide current_user to base page
@my_app.context_processor
def inject_user():
    return dict(user=current_user, zip=zip)


# Routes
@my_app.route('/', methods=['get', 'post'])
def index():
    # method POST
    if request.method == 'POST':
        # get transaction data from form
        transaction = Transaction(creditor=current_user.username.lower(),
                                  debtor=request.values.get('to').lower(),
                                  amount=request.values.get('amount'))

        if not user_exists(username=transaction.debtor):
            flash('User not exists')
            return redirect(url_for('main.index'))

        # get user balance
        blockchain = get_relative_blocks(current_user.username)
        balance = count_balance(blockchain, current_user.username)
        # check if transaction is valid
        if balance < transaction.amount:
            flash('Not enough LTC ( :')
            return redirect(url_for('main.index'))

        # get data about prev block
        previous_block = get_last_block()

        process_block.delay(dict(transaction), dict(previous_block))

        # render or redirect somewhere (Transaction will be added soon)

    # method GET
    if not current_user.is_authenticated:
        return render_template('hello.html')

    # get blockchain blocks relative to user and count balance
    blockchain = get_relative_blocks(current_user.username)
    balance = count_balance(blockchain, current_user.username)

    return render_template('index.html', blockchain=get_last_blocks(10), balance=balance)


@my_app.route('/register', methods=['get', 'post'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    # get data from form
    username = request.values.get('username').lower()
    email = request.values.get('email').lower()
    password = request.values.get('password')
    password_repeat = request.values.get('password_repeat')

    # validate form
    if password != password_repeat:
        flash('Passwords must be same')
        return render_template('register.html')

    if len(password) < 8:
        flash('Password must be more than 8 symbols')

    if user_exists(email=email):
        flash('User with this email already exists')
        return render_template('register.html')

    if user_exists(username=username):
        flash('User with this email already exists')
        return render_template('register.html')

    # create user
    create_user(username, password, email)
    flash('Success')

    # registration gift
    transaction = Transaction(creditor='God',
                              debtor=username,
                              amount=100)
    previous_block = get_last_block()
    if not previous_block:
        add_block(Block(id=0,
                        transaction={'creditor': 'God',
                                     'debtor': 'God',
                                     'amount': 0},
                        previous_block_hash='None',
                        hash='None',
                        proof=0))

    previous_block = get_last_block()
    process_block.delay(dict(transaction), dict(previous_block))
    return redirect(url_for('main.login'))


@my_app.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'POST':
        # grt data from form
        username = request.values.get('username').lower()
        password = request.values.get('password')
        remember_me = request.values.get('checkbox')

        # validate password
        user = get_user_by_login(username)
        password_hash = sha256(password.encode('utf-8')).hexdigest()

        # login user
        if user and user.password == password_hash:
            login_user(user, remember=remember_me)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid login or password')

    return render_template('login.html')


@my_app.route('/about')
def about():
    return render_template('about.html')


@my_app.route('/author')
def author():
    return render_template('author.html')


@my_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')

