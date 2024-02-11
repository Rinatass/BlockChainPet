from app import app
from app.views import my_app

app.register_blueprint(my_app)

if __name__ == '__main__':
    app.run()
