"""Эндпоинты для пользователей.
"""
from sanic import Blueprint, Request
from sanic_jwt.decorators import inject_user, protected

from src.core.decorators import admin_only, admin_or_owner_only
from src.core.responses import json_pydantic
from src.db.crud import create, get_exists_object, update_object
from src.db.models import MyUser as User
from src.schemas.users import (CreateSchema, PasswordSchema, ResponseSchema,
                               UpdateSchema)
from src.schemas.validators import validation

blue = Blueprint('users', url_prefix='/users')


@blue.get('/')
@inject_user()
@protected()
@admin_only
async def get_all_view(request: Request):
    """Прказать всех пользователей.
    """
    users = await User.all()
    return await json_pydantic(ResponseSchema, users, many=True)


@blue.get('/<user_id:int>')
@inject_user()
@protected()
@admin_or_owner_only
async def get_one_view(request: Request, user_id: int):
    """Показать пользователя c указанным `ID`.
    """
    user: User = await get_exists_object(user_id, User)
    return await json_pydantic(ResponseSchema, user)


@blue.post('/')
@inject_user()
@protected()
@admin_only
async def create_view(request: Request):
    """Создать нового пользователя.
    """
    user = await validation(request, CreateSchema)
    user: User = await create(user, User)
    return await json_pydantic(ResponseSchema, user)


@blue.patch('/active/<user_id:int>')
@inject_user()
@protected()
@admin_only
async def activation_view(request: Request, user_id: int):
    """Активировать/деактивировать пользователя c указанным `ID`.
    """
    user: User = await get_exists_object(user_id, User)
    user.active = not user.active
    await user.save()
    return await json_pydantic(ResponseSchema, user)


@blue.patch('/<user_id:int>')
@inject_user()
@protected()
@admin_only
async def update_view(request: Request, user_id: int):
    """Изменить пользователя c указанным `ID`.
    """
    user: User = await get_exists_object(user_id, User)
    update_data = await validation(request, UpdateSchema)
    await update_object(user, update_data, User)
    return await json_pydantic(ResponseSchema, user)


@blue.post('/change_password')
@inject_user()
@protected()
async def change_password(request: Request, user: User):
    """Изменить пароль пользователя c указанным `ID`.
    """
    password = await validation(request, PasswordSchema)
    await update_object(user, password, User)
    return await json_pydantic(ResponseSchema, user)
