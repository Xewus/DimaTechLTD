from jwt.api_jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from sanic import Blueprint, Request, json
from tortoise.exceptions import DoesNotExist

from src.core.exceptions import BadRequestException
from src.core.utils import make_activated_link
from src.db.crud import create, update_object
from src.db.models import User
from src.schemas.auth import CreateSchema, JWTSchema
from src.schemas.validators import validation
from src.settings import ALGORITHM, APP_KEY

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
    if not payload:
        return None
    user_id = payload.get('user_id', 0)
    user = await User.get_or_none(user_id=user_id)
    return user


@blue.get('/activate/<user_id:int>/<token:str>')
async def activation(request: Request, user_id: int, token: str):
    """Активироватоь нового пользователя по созданной ссылке."""
    try:
        payload = JWTSchema(
            **decode(
                jwt=token, key=APP_KEY, algorithms=[ALGORITHM]
            )
        )
        if user_id != payload.user_id:
            raise BadRequestException

        user: User = await User.get(pk=payload.user_id)

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


@blue.post('')
async def create_user(request: Request):
    """Создать нового пользователя."""
    user = await validation(request, CreateSchema)
    user: User = await create(user, User)
    link = make_activated_link(request, user.pk)
    return json(link)
