"""Функции и эндпоинты аутентификации и авторизации.
"""
from jwt.api_jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from sanic import Blueprint, Request, json
from tortoise.exceptions import DoesNotExist

from src.core.exceptions import BadRequestException
from src.core.utils import make_activated_link
from src.db.crud import create, get_exists_object, update_object
from src.db.models import MyUser as User
from src.schemas.auth import CreateSchema, JWTSchema
from src.schemas.validators import validation
from src.settings import AppSettings
from src.core.enums import AuthUrls

blue = Blueprint('login', url_prefix=AuthUrls.LOGIN)


async def authenticate(request: Request) -> User:
    """Аутентифицировать пользователя по юзеренейму и паролю,
    переданным в `JSON`е на эндпоинт `/auth`.
    Пользователь, прошедший проверку, получает`JWT`-токен.
    """
    if request.json is None:
        raise BadRequestException

    login_data = await validation(request, CreateSchema)
    user = await User.get_or_none(username=login_data['username'])

    if user is None or not user.active:
        raise BadRequestException

    if not user.verify_password(login_data['password']):
        raise BadRequestException

    return user


async def retrieve_user(request: Request, payload: dict):
    """Вернуть данные пользователя,
    отправившего запрос на эндпоинт `auth/me`.
    """
    if not payload:
        return None
    user_id = payload.get('user_id', 0)
    user = await User.get_or_none(user_id=user_id)
    return user


@blue.get('/activate/<user_id:int>/<token:str>')
async def activation(request: Request, user_id: int, token: str):
    """Активировать нового пользователя по созданной ссылке.
    Если ссылка устарела, выдать пользователю новую ссылку.
    Если пользователь уже активирован, вернуть ошибку.
    """
    try:
        payload = JWTSchema(
            **decode(
                jwt=token,
                key=AppSettings.APP_KEY,
                algorithms=[AppSettings.ALGORITHM]
            )
        )
        if user_id != payload.user_id:
            raise BadRequestException

        user: User = await get_exists_object(user_id, User)

    except InvalidSignatureError as err:
        raise BadRequestException(err.args)
    except ExpiredSignatureError as err:
        return json(
            {'msg': err.args[0]} | make_activated_link(request, user_id)
        )
    except DoesNotExist as err:
        raise BadRequestException(err.args)

    if user.active:
        raise BadRequestException('User %d is active' % user.pk)

    await update_object(user, {'active': True}, User)
    return json({'msg': 'User %s was activated' % user.username})


@blue.post('/')
async def create_user(request: Request):
    """Создать пользователя с юзернеймом и паролем, переданными в `JSON`.
    Вернуть пользователю временную ссылку для активации.
    """
    if not request.json:
        raise BadRequestException
    user = await validation(request, CreateSchema)
    user: User = await create(user, User)
    link = make_activated_link(request, user.pk)
    return json(link)
