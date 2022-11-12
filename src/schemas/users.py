from pydantic import BaseModel, Field

from .generics import UserIdSchema


class UserNameSchema(BaseModel):
    username: str = Field(
        description='Юзернейм пользователя',
        min_length=3,
        max_length=10
    )


class ResponseSchema(UserIdSchema, UserNameSchema):
    active: bool
    admin: bool

    class Config:
        orm_mode = True


class CreateSchema(UserNameSchema):
    password: str = Field(
        min_length=8
    )


class UpdateSchema(UserNameSchema):
    password: str | None
    active: bool | None
    admin: bool | None
