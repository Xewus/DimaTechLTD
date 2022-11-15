"""Эндпоинты для счетов.
"""
from sanic import Blueprint, Request
from sanic_jwt.decorators import inject_user, protected

from src.core.decorators import admin_only
from src.core.exceptions import ForbiddenException
from src.core.responses import json_pydantic
from src.db.crud import create, get_exists_object
from src.db.models import Bill
from src.db.models import MyUser as User
from src.schemas.bills import ResponseSchema

blue = Blueprint('bills', url_prefix='/bills')


@blue.get('/')
@inject_user()
@protected()
@admin_only
async def get_all_view(request: Request):
    """Показать все счета.
    """
    bills = await Bill.all()
    return await json_pydantic(ResponseSchema, bills, many=True)


@blue.get('/<bill_id:int>')
@inject_user()
@protected()
async def get_one_view(request: Request, user: User, bill_id: int):
    """Показать счёт c указанным `ID`.
    """
    bill: Bill = await get_exists_object(bill_id, Bill)

    if not user.admin and user.user_id != bill.user:
        raise ForbiddenException

    return await json_pydantic(ResponseSchema, bill)


@blue.get('/user/<user_id:int>')
@inject_user()
@protected()
@admin_only
async def get_user_view(request: Request, user_id: int):
    """Показать счета пользователя c указанным `ID`.
    """
    bills = await Bill.filter(user_id=user_id)
    return await json_pydantic(ResponseSchema, bills, many=True)


@blue.get('/my')
@inject_user()
@protected()
async def get_my_view(request: Request, user: User):
    """Показать пользователю его счета.
    """
    bills = await Bill.filter(user_id=user.pk)
    return await json_pydantic(ResponseSchema, bills, many=True)


@blue.post('/')
@inject_user()
@protected()
async def create_view(request: Request, user: User):
    """Создать счёт привязанный к пользователю, отправившему запрос.
    """
    bill = {'user_id': user.user_id}
    bill: Bill = await create(bill, Bill)
    return await json_pydantic(ResponseSchema, bill)
