from pydantic_settings import BaseSettings
from pydantic import Field
from exceptions import SettingsTypeError

'''Pydantics_settings reads settings from environment variables'''

class AppSettings(BaseSettings):
    debug: bool = Field(default=False)

class DatabaseSettings(BaseSettings):
    db_login: str
    db_password: str

class SettingsFactory:
    def get_settings(self, type:str):
        if type == 'app':
            return AppSettings()
        if type == 'db':
            return DatabaseSettings()
        else:
            raise SettingsTypeError("Settings type not correct")
