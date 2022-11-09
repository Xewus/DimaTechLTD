"""Эндпоинты для пользователей.
"""
from sanic import Blueprint, Request, json
from sanic_ext import validate
from tortoise.exceptions import IntegrityError

from src.core.utils import json_response
from src.db.models import User
from src.schemas.users import (UserCreateSchema, UserResponseSchema,
                               UserUpdateSchema)

blue = Blueprint('users', url_prefix='/users')


@blue.get('/')
async def get_all_users(request: Request):
    users = await User.all()
    return await json_response(UserResponseSchema, users, many=True)


@blue.post('/')
@validate(json=UserCreateSchema, body_argument='new_user')
async def create_user(request: Request, new_user: UserCreateSchema):
    user = new_user.dict()
    try:
        user = await User.create(**user)
    except IntegrityError:
        return json({'detail': new_user.username}, status=422)
    return await json_response(UserResponseSchema, user)


@blue.patch('/active/<username:str>')
async def activ(request: Request, username: str):
    user = await User.get_or_none(username=username)
    if user is None:
        return json({'detail': 'username'}, status=422)
    user.active = not user.active
    await user.save()
    return await json_response(UserResponseSchema, user)


@blue.patch('/<username:str>')
@validate(json=UserUpdateSchema, body_argument='update_data')
async def update_user(request: Request, username: str, update_data: UserUpdateSchema):
    user: User = await User.get_or_none(username=username)
    if user is None:
        return json({'detail': 'username'}, status=422)
    user.update_from_dict(update_data.dict(exclude_none=True))
    await user.save()
    return await json_response(UserResponseSchema, user)


@blue.get('/me')
async def me(request: Request):
    user = await User.get(user_id=1)
    return await json_response(UserResponseSchema, user)


@blue.post('/login')
async def login(request: Request):
    return json({'Bearer': 'kjklk'})
