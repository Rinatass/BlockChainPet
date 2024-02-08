from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from .models import Base
from config import SettingsFactory

db_settings = SettingsFactory().get_settings('db')
db_engine = create_engine(f"postgresql+psycopg2://"
                          f"{db_settings.db_login}:{db_settings.db_password}"
                          f"@{db_settings.db_host}:{db_settings.db_port}/mydb", echo=True)

if not(database_exists(db_engine.url)):
    create_database(db_engine.url)

Base.metadata.drop_all(bind=db_engine)
Base.metadata.create_all(bind=db_engine)

app = Flask(__name__)


from . import views