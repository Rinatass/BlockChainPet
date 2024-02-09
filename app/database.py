from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from .models import Base, User
from config import SettingsFactory

db_settings = SettingsFactory().get_settings('db')
db_engine = create_engine(f"postgresql+psycopg2://"
                          f"{db_settings.db_login}:{db_settings.db_password}"
                          f"@{db_settings.db_host}:{db_settings.db_port}/mydb", echo=True)

session_factory = sessionmaker(db_engine)

class Database:
    def create_user(self, username, password, email):
        user = User(username=username, email=email, password=password)
        with session_factory() as s:
            s.add(user)
            s.commit()

    def user_exists(username, email):
        with session_factory() as s:
            query = select(User).where(User.email == email)
            res = s.execute(query)
            if res.one_or_none():
                return True
        return False




'''if not(database_exists(db_engine.url)):
    create_database(db_engine.url)

Base.metadata.drop_all(bind=db_engine)
Base.metadata.create_all(bind=db_engine)'''