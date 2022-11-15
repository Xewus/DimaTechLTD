from pydantic import BaseModel


class AppSettings(BaseModel):
    DEBUG: bool = False
    HOST: str = 'localhost'
    PORT: int = 9999
    APP_NAME: str = 'TestApp'
    APP_KEY: str ='testappkey'
    SANIC_JWT_ACCESS_TOKEN_NAME: str = 'access_token'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE: int = 60 * 60 * 24
    ACTIVATE_TOKEN_EXPIRE: int = 60 * 15

    DB_URL: str = 'sqlite://./db.sqlite'
    DB_MODULES: dict[str, list[str]] = {'models': ['src.db.models']}


class FirstUser(BaseModel):
    username: str = 'AdminUser'
    password: str = 'password'
    active: bool = True
    admin: bool = True


AppSettings: BaseModel= AppSettings()
FirstUser: BaseModel = FirstUser()
