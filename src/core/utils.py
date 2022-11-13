"""Вспомогательные функции.
"""
from hashlib import sha1
from time import time

from jwt.api_jwt import encode
from sanic import Request

from src.schemas.auth import UrlSchema
from src.settings import AppSettings


def make_signature(values: dict) -> str:
    """Сделать сигнатуру транзакции.
    """
    app_key = AppSettings.APP_KEY
    transaction_id = values.get('transaction_id', 1)
    user_id = values.get('user_id', 2)
    bill_id = values.get('bill_id', 3)
    amount = values.get('amount', 4)
    sign = sha1()

    sign.update(
        f"{app_key}:{transaction_id}:{user_id}:{bill_id}:{amount}".encode()
    )
    return sign.hexdigest()


def make_activated_link(request: Request, user_id: int) -> dict:
    """Сделать ссылку для активации пользователя.
    """
    payload = {
        'user_id': user_id,
        'exp': time() + AppSettings.ACCESS_TOKEN_EXPIRE
    }
    link = request.url_for(
        view_name='login.activation',
        user_id=user_id,
        token=encode(
            payload=payload,
            key=AppSettings.APP_KEY,
            algorithm=AppSettings.ALGORITHM
        )
    )
    return UrlSchema(url=link).dict()
