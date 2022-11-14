"""Декораторы для обслуживания приложения.
"""
from functools import wraps

from sanic import Request

from src.core.exceptions import ForbiddenException
from src.db.models import MyUser as User


def admin_only(wrapped):
    """Разрешить доступ только админам.
    """
    def decorator(f):
        @wraps(f)
        async def decorated_function(
            request: Request, user: User, *args, **kwargs
        ):
            if not user.admin:
                raise ForbiddenException
            return await f(request, *args, **kwargs)
        return decorated_function
    return decorator(wrapped)


def admin_or_owner_only(wrapped):
    """Разрешить доступ только админам или пользователям с указанным `ID`.
    """
    def decorator(f):
        @wraps(f)
        async def decorated_function(
            request: Request, user: User, *args, **kwargs
        ):
            if not (user.admin or user.user_id == kwargs.get('user_id', 0)):
                raise ForbiddenException
            return await f(request, *args, **kwargs)
        return decorated_function
    return decorator(wrapped)
