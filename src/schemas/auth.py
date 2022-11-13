from time import time

from pydantic import BaseModel, Field, HttpUrl, validator

from src.core.exceptions import BadRequestException
from src.settings import AppSettings

from .generics import UserIdSchema
from .users import CreateSchema


class CreateSchema(CreateSchema):
    """Схема данных для создания пользователя.

    #### Fields:
    - username (str): Юзернейм пользователя.
    - password (str): Пароль пользователя.
    """
    ...


class UrlSchema(BaseModel):
    """Схема данных для `HTTP`-ссылки.

    #### Fields:
    - url (HttpUrl): HTTP-ссылка.
    """
    url: HttpUrl = Field(
        description='`HTTP`-ссылка'
    )


class JWTSchema(UserIdSchema):
    """Схема данных `JWT`-токена.

    #### Fields:
    - user_id (PositivInt): Идентификатор пользователя.
    - exp (float): Окончание срока действия токена в формате `UNIXTIME.
    """
    exp: float = Field(
        description='Окончание срока действия токена в формате `UNIXTIME`'
    )

    @validator('exp')
    def validate(cls, exp: float) -> float:
        """Проверить, что время не превышает допустимое.
        """
        if exp > time() + AppSettings.ACTIVATE_TOKEN_EXPIRE:
            raise BadRequestException
        return exp
