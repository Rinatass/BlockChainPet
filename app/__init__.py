from flask import Flask
from flask_login import LoginManager
from app.config import SettingsFactory
from app.models import User
from app.database import get_user_by_id

app = Flask(__name__)

app_settings = SettingsFactory().get_settings('app')
debug = app_settings.debug

app.config['SECRET_KEY'] = app_settings.secret_key
app.config['DEBUG'] = debug

login_manager = LoginManager(app)
login_manager.login_view = 'main.login'


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)
