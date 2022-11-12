from time import time

from pydantic import BaseModel, HttpUrl, validator

from src.core.exceptions import BadRequestException
from src.settings import ACTIVATE_TOKEN_EXPIRE

from .generics import UserIdSchema
from .users import CreateSchema


class CreateSchema(CreateSchema):
    ...


class UrlSchema(BaseModel):
    url: HttpUrl


class JWTSchema(UserIdSchema):
    exp: float

    @validator('exp')
    def validate(cls, exp: float) -> float:
        if exp > time() + ACTIVATE_TOKEN_EXPIRE:
            raise BadRequestException
        return exp
