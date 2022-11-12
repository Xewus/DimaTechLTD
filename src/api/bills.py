"""Эндпоинты для счетов.
"""
from sanic import Blueprint, Request
from sanic_jwt.decorators import inject_user, protected

from src.core.decorators import admin_only, admin_or_owner_only
from src.core.exceptions import ForbiddenException
from src.core.views import json_response
from src.db.crud import create, update_object
from src.db.models import Bill, User
from src.schemas.bills import CreateSchema, ResponseSchema, UpdateSchema
from src.schemas.validators import get_exists_object, validation

blue = Blueprint('bills', url_prefix='/bills')


@blue.get('/')
@inject_user()
@protected()
@admin_only
async def get_all_view(request: Request):
    """Показать все счета."""
    bills = await Bill.all()
    return await json_response(ResponseSchema, bills, many=True)


@blue.get('/<bill_id:int>')
@inject_user()
@protected()
async def get_one_view(request: Request, user: User, bill_id: int):
    """Показать указанный счёт."""
    bill: Bill = await get_exists_object(bill_id, Bill)
    if not user.admin and user.user_id != bill.user:
        raise ForbiddenException
    return await json_response(ResponseSchema, bill)


@blue.get('/user/<user_id:int>')
@inject_user()
@protected()
@admin_or_owner_only
async def get_my_view(request: Request, user_id: int):
    """Показать счета указанного пользователя"""
    await get_exists_object(user_id, User)
    bills = await Bill.filter(user_id=user_id)
    return await json_response(ResponseSchema, bills, many=True)


@blue.post('/')
@inject_user()
@protected()
async def create_view(request: Request, user: User):
    """Создать новый счёт."""
    bill = {'user_id': user.user_id}
    if request.json:
        bill.update(await validation(request, CreateSchema))
    bill: Bill = await create(bill, Bill)
    return await json_response(ResponseSchema, bill)


@blue.patch('/<bill_id:int>')
@inject_user()
@protected()
@admin_only
async def update_view(request: Request, bill_id: int):
    """Изменить счёт."""
    bill: Bill = await get_exists_object(bill_id, Bill)
    update_data = await validation(request, UpdateSchema)
    await update_object(bill, update_data, Bill)
    return await json_response(ResponseSchema, bill)
