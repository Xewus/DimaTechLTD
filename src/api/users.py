"""Эндпоинты для пользователей.
"""
from sanic import Blueprint, Request, json

from src.core.views import json_response
from src.db.crud import create, update_object
from src.db.models import User
from src.schemas.users import CreateSchema, ResponseSchema, UpdateSchema
from src.schemas.validators import get_exists_object, validation
from src.core.decorators import admin_only, admin_or_owner_only
from sanic_jwt.decorators import protected, inject_user

blue = Blueprint('users', url_prefix='/users')


@blue.get('/')
@inject_user()
@protected()
@admin_only
async def get_all_view(request: Request, **_):
    """Прказать всех пользователей."""
    users = await User.all()
    return await json_response(ResponseSchema, users, many=True)


@blue.get('/<user_id:int>')
@inject_user()
@protected()
@admin_or_owner_only
async def get_one_view(request: Request, **kwargs):
    """Показать указанного пользователя."""
    user = await get_exists_object(kwargs.get('user_id', 0), User)
    return await json_response(ResponseSchema, user)


@blue.post('/')
async def create_view(request: Request):
    """Создать нового пользователя."""
    user = await validation(request, CreateSchema)
    user = await create(user, User)
    return await json_response(ResponseSchema, user)


@blue.patch('/active/<user_id:int>')
@inject_user()
@protected()
@admin_only
async def activation_view(request: Request, user_id: int, **_):
    "Активировать/деактивировать пользователя."
    user = await get_exists_object(user_id, User)
    user.active = not user.active
    await user.save()
    return await json_response(ResponseSchema, user)


@blue.patch('/<user_id:int>')
@inject_user()
@protected()
@admin_only
async def update_view(request: Request, user_id: int, **_):
    """Изменить пользователя."""
    user = await get_exists_object(user_id, User)
    update_data = await validation(request, UpdateSchema)
    await update_object(user, update_data, User)
    return await json_response(ResponseSchema, user)
