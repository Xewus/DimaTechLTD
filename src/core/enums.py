from enum import Enum


class AuthUrls(str, Enum):
    AUTH = '/auth'
    LOGIN = '/login'
    ACTIVATE = '/activate'
