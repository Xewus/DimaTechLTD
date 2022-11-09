"""Эндпоинты для пользователей.
"""
from sanic import Blueprint, Request
from sanic.response import HTTPResponse, json
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)
from tortoise.exceptions import IntegrityError

from src.db.models import User
from src.generics.views import ApiGetMixin, ApiPatchMixin, ApiPosMixin

blue = Blueprint('users', url_prefix='/users')

UserPyd = pydantic_model_creator(User)
UserPydList = pydantic_queryset_creator(User)



class UserView(ApiGetMixin, ApiPosMixin, ApiPatchMixin):
    model = User
    one = True
    many = True


@blue.route('/me')
async def me(request: Request) -> HTTPResponse:
    user = await UserPyd.from_queryset_single(User.get(user_id=1))
    return json(user.dict())


@blue.route('/login', methods=['POST'])
async def login(request: Request) -> HTTPResponse:
    return json({'Bearer': 'kjklk'})


@blue.route('/activ/<username:str>', methods=['PATCH'])
async def activ(request: Request, username: str) -> HTTPResponse:
    user = await User.get_or_none(username=username)
    if user is None:
        return json({'detail': 'username'}, status=422)
    user.active = not user.active
    await user.save()
    user = await UserPyd.from_tortoise_orm(user)
    return json(user.dict())


blue.add_route(
    handler=UserView.as_view(),
    uri='/all',
    methods=['GET']
)
blue.add_route(
    handler=UserView.as_view(),
    uri='/<pk:int>',
    methods=['GET', 'PATCH']
)
blue.add_route(
    handler=UserView.as_view(),
    uri='/',
    methods=['POST']
)
