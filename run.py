from app import app
from app.views import my_app
from app.config import SettingsFactory

settings = SettingsFactory().get_settings('app')


app.register_blueprint(my_app)

if __name__ == '__main__':
    app.run(host=settings.host, port=settings.port)
