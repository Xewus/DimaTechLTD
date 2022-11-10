"""Эндпоинты для пользователей.
"""
from sanic import Blueprint, Request, json
from sanic_ext import validate
from tortoise.exceptions import IntegrityError

from src.core.utils import json_response
from src.db.models import Bill, User
from src.schemas.users import (UserCreateSchema, UserResponseSchema,
                               UserUpdateSchema)

blue = Blueprint('users', url_prefix='/users')


@blue.get('/')
async def get_all_users(request: Request):
    """Прказать всех пользователей."""
    users = await User.all()
    return await json_response(UserResponseSchema, users, many=True)


@blue.get('/<user_id:int>')
async def get_user(request: Request, user_id: int):
    """Показать указанного пользователя."""
    user: User = await User.get_or_none(pk=user_id).select_related('bills')
    if user is None:
        return json({'detail': 'username'}, status=422)
    return await json_response(UserResponseSchema, user)


@blue.post('/')
@validate(json=UserCreateSchema, body_argument='new_user')
async def create_user(request: Request, new_user: UserCreateSchema):
    """Создать нового пользователя."""
    user = new_user.dict(exclude_none=True)
    try:
        user = await User.create(**user)
    except IntegrityError:
        return json({'detail': 'username'}, status=422)
    return await json_response(UserResponseSchema, user)


@blue.patch('/active/<user_id:int>')
async def activ(request: Request, user_id: int):
    "Активировать/деактивировать пользователя."
    user = await User.get_or_none(pk=user_id)
    if user is None:
        return json({'detail': 'username'}, status=422)
    user.active = not user.active
    await user.save()
    return await json_response(UserResponseSchema, user)


@blue.patch('/<user_id:int>')
@validate(json=UserUpdateSchema, body_argument='update_data')
async def update_user(request: Request, user_id: int, update_data: UserUpdateSchema):
    """Изменить пользователя."""
    user: User = await User.get_or_none(pk=user_id)
    if user is None:
        return json({'detail': 'username'}, status=422)
    user.update_from_dict(update_data.dict(exclude_none=True))
    await user.save()
    return await json_response(UserResponseSchema, user)


@blue.get('/me')
async def me(request: Request):
    """Показать данные о себе."""
    user = await User.get(user_id=1)
    return await json_response(UserResponseSchema, user)


@blue.post('/login')
async def login(request: Request):
    """Залогиниться."""
    return json({'Bearer': 'kjklk'})
