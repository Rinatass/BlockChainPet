from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import sessionmaker
from hashlib import sha256
from .models import User
from config import SettingsFactory

db_settings = SettingsFactory().get_settings('db')
db_engine = create_engine(f"postgresql+psycopg2://"
                          f"{db_settings.db_login}:{db_settings.db_password}"
                          f"@{db_settings.db_host}:{db_settings.db_port}/mydb", echo=True)

session_factory = sessionmaker(db_engine)


def create_user(username, password, email):
    password = sha256(password.encode('utf-8')).hexdigest()
    user = User(username=username, email=email, password=password)
    with session_factory() as s:
        s.add(user)
        s.commit()


def user_exists(email):
    with session_factory() as s:
        query = select(User).where(User.email == email)
        res = s.execute(query)
        if res.one_or_none():
            return True
    return False


def get_user_by_id(id):
    with session_factory() as s:
        query = select(User).where(User.id == id)
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
