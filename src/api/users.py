"""Эндпоинты для пользователей.
"""
from sanic import Blueprint, Request, json

from src.core.views import json_response
from src.db.crud import create, update_object
from src.db.models import User
from src.schemas.users import CreateSchema, ResponseSchema, UpdateSchema
from src.schemas.validators import get_exists_object, validation

blue = Blueprint('users', url_prefix='/users')


@blue.get('/')
async def get_all_view(request: Request):
    """Прказать всех пользователей."""
    users = await User.all()
    return await json_response(ResponseSchema, users, many=True)


@blue.get('/<user_id:int>')
async def get_one_view(request: Request, user_id: int):
    """Показать указанного пользователя."""
    user = await get_exists_object(user_id, User)
    return await json_response(ResponseSchema, user)


@blue.post('/')
async def create_view(request: Request):
    """Создать нового пользователя."""
    user = await validation(request, CreateSchema)
    user = await create(user, User)
    return await json_response(ResponseSchema, user)


@blue.patch('/active/<user_id:int>')
async def activation_view(request: Request, user_id: int):
    "Активировать/деактивировать пользователя."
    user = await get_exists_object(user_id, User)
    user.active = not user.active
    await user.save()
    return await json_response(ResponseSchema, user)


@blue.patch('/<user_id:int>')
async def update_view(request: Request, user_id: int):
    """Изменить пользователя."""
    user = await get_exists_object(user_id, User)
    update_data = await validation(request, UpdateSchema)
    await update_object(user, update_data, User)
    return await json_response(ResponseSchema, user)


@blue.get('/me')
async def get_me_view(request: Request):
    """Показать данные о себе."""
    user = await User.get(user_id=1)
    return await json_response(ResponseSchema, user)


@blue.post('/login')
async def login_view(request: Request):
    """Залогиниться."""
    return json({'Bearer': 'kjklk'})
