from hashlib import sha1
from time import time

from jwt.api_jwt import encode
from sanic import Request

from src.schemas.auth import UrlSchema
from src.settings import ACTIVATE_TOKEN_EXPIRE, ALGORITHM, APP_KEY


def make_signature(values: dict) -> str:
    """Сделать сигнатуру транзакции при покупке товара."""
    sign = sha1()
    sign.update(
        f"{APP_KEY}:{values['bill_id']}:{values['amount']}".encode()
    )
    return sign.hexdigest()


def make_activated_link(request: Request, user_id: int) -> dict:
    """Сделать ссылку для активации пользователя."""
    payload = {
        'user_id': user_id,
        'exp': time() + ACTIVATE_TOKEN_EXPIRE
    }
    link = request.url_for(
        view_name='login.activation',
        user_id=user_id,
        token=encode(payload=payload, key=APP_KEY, algorithm=ALGORITHM)
    )
    return UrlSchema(url=link).dict()
