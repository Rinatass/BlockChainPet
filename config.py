from pydantic_settings import BaseSettings
from pydantic import Field
from exceptions import SettingsTypeError

class AppSettings(BaseSettings):
    debug: bool = Field(default=False)

class SettingsFactory:
    def get_settings(self, type:str):
        if type == 'app':
            return AppSettings()
        else:
            raise SettingsTypeError("Settings type not correct")
