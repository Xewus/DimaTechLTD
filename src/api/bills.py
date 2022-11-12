"""Эндпоинты для счетов.
"""
from sanic import Blueprint, Request

from src.core.views import json_response
from src.db.crud import create, update_object
from src.db.models import Bill, User
from src.schemas.bills import CreateSchema, ResponseSchema, UpdateSchema
from src.schemas.validators import get_exists_object, validation
from src.core.decorators import admin_only, admin_or_owner_only
from sanic_jwt.decorators import protected, inject_user
from src.core.exceptions import ForbiddenException

blue = Blueprint('bills', url_prefix='/bills')


@blue.get('/')
@inject_user()
@protected()
@admin_only
async def get_all_view(request: Request, **_):
    """Показать все счета."""
    bills = await Bill.all()
    return await json_response(ResponseSchema, bills, many=True)


@blue.get('/<bill_id:int>')
@inject_user()
@protected()
async def get_one_view(request: Request, user: User, bill_id: int, **_):
    """Показать указанный счёт."""
    bill: Bill = await get_exists_object(bill_id, Bill)
    if not(user.admin or not bill or user.user_id != bill.user):
        raise ForbiddenException
    return await json_response(ResponseSchema, bill)


@blue.get('/user/<user_id:int>')
async def get_my_view(request: Request, user_id: int):
    """Показать счета указанного пользователя"""
    await get_exists_object(user_id, User)
    bills = await Bill.filter(user_id=user_id)
    return await json_response(ResponseSchema, bills, many=True)


@blue.post('/')
async def create_view(request: Request):
    """Создать новый счёт."""
    bill = await validation(request, CreateSchema)
    bill: Bill = await create(bill, Bill)
    return await json_response(ResponseSchema, bill)


@blue.patch('/<bill_id:int>')
async def update_view(request: Request, bill_id: int):
    """Изменить счёт."""
    bill: Bill = await get_exists_object(bill_id, Bill)
    update_data = await validation(request, UpdateSchema)
    await update_object(bill, update_data, Bill)
    return await json_response(ResponseSchema, bill)
