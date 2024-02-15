from pydantic_settings import BaseSettings
from pydantic import Field
from app.exceptions import SettingsTypeError

'''Pydantics_settings reads settings from environment variables'''


class AppSettings(BaseSettings):
    debug: bool = Field(default=False)
    secret_key: str = Field(default=None)
    host: str = Field(default='localhost')
    port: str = Field(default='5000')


class DatabaseSettings(BaseSettings):
    db_login: str = Field(default=None)
    db_password: str = Field(default=None)
    db_host: str = Field(default=None)
    db_port: str = Field(default=None)


class CelerySettings(BaseSettings):
    celery_name: str = Field(default='celery_worker')
    celery_broker: str = Field(default='redis://localhost')


class MongoSettings(BaseSettings):
    mongo_url: str = Field(default='localhost')
    mongo_port: int = Field(default=27017)
    mongo_login: str
    mongo_password: str


class SettingsFactory:
    def get_settings(self, type_):
        if type_ == 'app':
            return AppSettings()
        if type_ == 'db':
            return DatabaseSettings()
        if type_ == 'celery':
            return CelerySettings()
        if type_ == 'mongo':
            return MongoSettings()
        else:
            raise SettingsTypeError("Settings type not correct")
