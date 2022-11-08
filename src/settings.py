from pathlib import Path
from decouple import config

DEBUG = config('DEBUG', default=True)

BASE_DIR = Path(__file__).resolve().resolve

APP_NAME = config('APP_NAME', default='Application')
DB_SETTINGS = {}
