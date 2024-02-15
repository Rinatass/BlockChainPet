from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from hashlib import sha256
from app.config import SettingsFactory
from app.exceptions import KeyWordArgsError
from app.models import User, Base

db_settings = SettingsFactory().get_settings('db')
db_engine = create_engine(f"postgresql+psycopg2://"
                          f"{db_settings.db_login}:{db_settings.db_password}"
                          f"@{db_settings.db_host}:{db_settings.db_port}/mydb", echo=False)

if not database_exists(db_engine.url):
    create_database(db_engine.url)

Base.metadata.create_all(db_engine)

session_factory = sessionmaker(db_engine)


def create_user(username, password, email):
    password = sha256(password.encode('utf-8')).hexdigest()
    user = User(username=username, email=email, password=password)
    with session_factory() as s:
        s.add(user)
        s.commit()


def user_exists(email=None, username=None):
    if email:
        email = email.lower()
        with session_factory() as s:
            query = select(User).where(User.email == email)
            res = s.execute(query)
            if res.one_or_none():
                return True
        return False
    if username:
        username = username.lower()
        with session_factory() as s:
            query = select(User).where(User.username == username)
            res = s.execute(query)
            if res.one_or_none():
                return True
        return False
    raise KeyWordArgsError('Please indicate user or email in keywords')


def get_user_by_id(id_):
    with session_factory() as s:
        query = select(User).where(User.id == id_)
        res = s.execute(query)
        user = res.scalar_one_or_none()

    if user:
        return user
    return False


def get_user_by_login(login):
    with session_factory() as s:
        query = select(User).filter((User.username == login) | (User.email == login))
        res = s.execute(query)
        user = res.scalar_one_or_none()
    return user
