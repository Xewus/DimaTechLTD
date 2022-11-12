from sanic import Blueprint, Request, json
from functools import wraps

from src.core.exceptions import BadRequestException
from src.core.views import json_response
from src.db.crud import create, update_object
from src.db.models import User
from src.schemas.users import CreateSchema, ResponseSchema, UpdateSchema
from src.schemas.validators import validation

blue = Blueprint('login', url_prefix='/login')

async def authenticate(request: Request) -> User:
    if request.json is None:
        raise BadRequestException
    login_data = await validation(request, CreateSchema)
    user = await User.get_or_none(username=login_data['username'])
    if user is None or not user.active:
        raise BadRequestException('Auth')

    if not user.verify_password(login_data['password']):
        raise BadRequestException('Auth')

    return user

async def retrieve_user(request: Request, payload: dict):
    if payload:
        user_id = payload.get('user_id', None)
        user = await User.get(user_id=user_id)
        return user
    else:
        return None


def authenticated(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            print('\n'*3, request.headers.get('Authorization', 111), '\n'*5)
            return await f(request, *args, **kwargs)
        return decorated_function
    return decorator(wrapped)


@blue.get('/<token:str>')
async def activation(request: Request, token: str):
    ...


# @blue.post('/')
# async def create_user(request: Request):
#     """Создать нового пользователя."""
#     user = await validation(request, CreateSchema)
#     user = await create(user, User)
#     return await json_response(ResponseSchema, user)


# def set_request_user(wrapped):
#     def decorator(fn):
#         @wraps(fn)
#         async def decorated_function(request: Request, *args, **kwargs):
#             request.ctx.user.is_authenticated = check_token(request)
#         return decorated_function
#     return decorator(wrapped)