from app import app
from config import SettingsFactory


if __name__ == '__main__':
    app_settings = SettingsFactory().get_settings('app'
    )
    debug = app_settings.debug
    app.config['SECRET_KEY'] = app_settings.secret_key
    app.run(debug = debug)
