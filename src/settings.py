from pathlib import Path

from decouple import config
from pydantic import BaseSettings, PostgresDsn

BASE_DIR = Path(__file__).resolve().parent.parent

class EnvSettings(BaseSettings):

    class Config:
        env_file = BASE_DIR / 'env'


class AppSettings(EnvSettings):
    DEBUG: bool
    HOST: str
    PORT: int
    APP_NAME: str
    APP_KEY: str
    SANIC_JWT_ACCESS_TOKEN_NAME: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE: int = 60 * 60 * 24
    ACTIVATE_TOKEN_EXPIRE: int = 60 * 15

    DB_URL: PostgresDsn = config('DB_URL')
    DB_MODULES: dict[str, list[str]] = {'models': ['src.db.models']}

    class Config:
        env_file = '.env'


class FirstUser(EnvSettings):
    username: str
    password: str = config('PASSWORD')
    active: bool = True
    admin: bool = True


AppSettings: BaseSettings = AppSettings()
FirstUser: BaseSettings = FirstUser()


MAX_LEN_USERNAME = 10
MIN_LEN_PASSWORD = 8


TORTOISE_ORM = {
    'connections': {
        'default': AppSettings.DB_URL,
    },
    'apps': {
        'models': {
            'models': ['src.db.models'],
            'default_connection': 'default'
        },
    },
}


# ################################# author ################################# #

AUTHOR = {
    'name': 'xewus',
    'email': 'xewuss@yandex.ru',
    'url': 'https://github.com/Xewus'
}
