from pydantic import BaseModel, Field

from .generics import UserIdSchema


class UserNameSchema(BaseModel):
    """Схема данных для юзернейма пользователя.

    #### Fields:
    - username (str): Юзернейм пользователя.
    """
    username: str = Field(
        description='Юзернейм пользователя',
        min_length=3,
        max_length=10
    )


class PasswordSchema(BaseModel):
    """Схема данных для пароля пользователя.

    #### Fields:
    - password (str): Пароль пользователя.
    """
    password: str = Field(
        description='Пароль пользователя',
        min_length=8
    )


class ResponseSchema(UserIdSchema, UserNameSchema):
    """Схема данных для создания пользователя.

    #### Fields:
    - user_id (PositivInt): Идентификатор пользователя.
    - username (str): Юзернейм пользователя.
    - active (bool): Активен ли пользователь.
    - admin (bool): Является ли пользователь админом.
    """
    active: bool = Field(
        description='Активен ли пользователь'
    )
    admin: bool = Field(
        description='Является ли пользователь админом'
    )

    class Config:
        orm_mode = True


class CreateSchema(UserNameSchema, PasswordSchema):
    """Схема данных для создания пользователя.

    #### Fields:
    - username (str): Юзернейм пользователя.
    - password (str): Пароль пользователя.
    """
    ...


class UpdateSchema(UserNameSchema):
    """Схема данных для изменения пользователя.

    #### Fields:
    - password (str | None): Пароль пользователя.
    - active (bool | None): Активен ли пользователь.
    - admin (bool | None): Является ли пользователь админом.
    """
    password: str | None
    active: bool | None
    admin: bool | None
