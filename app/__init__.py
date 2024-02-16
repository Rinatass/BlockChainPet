from flask import Flask
from flask_login import LoginManager
from app.config import SettingsFactory
from app.models import User
from app.database import get_user_by_id
from app.views import my_app

app = Flask(__name__)
app.register_blueprint(my_app)

# get settings from config
app_settings = SettingsFactory().get_settings('app')
debug = app_settings.debug

app.config['SECRET_KEY'] = app_settings.secret_key
app.config['DEBUG'] = debug


# create flask-login manager
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'


@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)
    return user

