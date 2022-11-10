from pathlib import Path

from decouple import config
from sanic.config import Config

DEBUG = config('DEBUG', default=False, cast=bool)

BASE_DIR = Path(__file__).resolve().resolve

APP_NAME = config('APP_NAME', default='Application')
APP_KEY = config('APP_KEY', default='appkey')

class AppConfig(Config):
    DEBUG = True
    # RELOAD_START = DEBUG
    HOST = config('HOST', default='127.0.0.1')
    PORT = config('PORT', default=8000, cast=int)
    WORKERS = config('WORKERS', default=2, cast=int)

DB_URL='postgresql://postgres:postgres@localhost/postgres'

SECRET_KEY = config('SECRET_KEY', default='secretkey')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

MAX_LEN_USERNAME = 10
MIN_LEN_PASSWORD = 8
################### database ####################
FIRST_USER = {
    'username': config('USERNAME', default='User').capitalize(),
    'email': config('EMAIL', default='q@q.qq'),
    'password': config('FIRST_USER_PASSWORD', default='12345678'),
    'active': True,
    'admin': True
}

TORTOISE_CONFIG = {
    'db_url': 'sqlite://./db.sqlite',# config('DB_URL', default='sqlite:///data/db.sqlite'),
    'modules': {'models': ['src.db.models']},
    'generate_schemas': True
}

TORTOISE_ORM = {
    "connections": {
        "default": TORTOISE_CONFIG['db_url'],
    },
    "apps": {
        "models": {"models": ['src.db.models'], "default_connection": "default"},
    },
}

#####################################################################3

AUTHOR = {
    'name': 'xewus',
    'email': 'xewuss@yandex.ru',
    'url': 'https://github.com/Xewus'
}