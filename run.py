from app import app
from config import SettingsFactory

settings_factory = SettingsFactory()

if __name__ == '__main__':
    debug = settings_factory.get_settings('app').debug
    print(debug)
    app.run(debug = debug)
