"""Эндпоинты для транзакций.
"""
from sanic import Blueprint, Request
from sanic.response import json
from sanic_jwt.decorators import inject_user, protected

from src.core.decorators import admin_only, admin_or_owner_only
from src.core.exceptions import ForbiddenException
from src.core.views import json_response
from src.db.crud import create_transaction
from src.db.models import Bill, Transaction, User
from src.schemas.transactions import CreateSchema, ResponseSchema
from src.schemas.validators import get_exists_object, validation
from src.settings import DEBUG

blue = Blueprint('transactions', url_prefix='/payment')


@blue.get('/')
@inject_user()
@protected()
@admin_only
async def get_all_view(request: Request):
    """Показать все транзакции."""
    transactions = await Transaction.all()
    return await json_response(ResponseSchema, transactions, many=True)


@blue.get('/<transaction_id:int>')
@inject_user()
@protected()
async def get_one_view(request: Request, user: User, transaction_id: int):
    """Показать указанного транзакцию."""
    transaction = await get_exists_object(transaction_id, Transaction)
    if not user.admin and user.user_id != transaction.user:
        raise ForbiddenException
    return await json_response(ResponseSchema, transaction)


@blue.get('/user/<user_id:int>')
@inject_user()
@protected()
@admin_or_owner_only
async def get_user_transactions(request: Request, user_id: int):
    """Показать транзакции указанного пользователя."""
    await get_exists_object(user_id, User)
    transactions = await Transaction.filter(user_id=user_id)
    return await json_response(ResponseSchema, transactions, many=True)


@blue.get('/bill/<bill_id:int>')
@inject_user()
@protected()
async def get_bill_transactions(request: Request, user: User, bill_id: int):
    """Показать транзакции указанного счётв."""
    bill: Bill = await get_exists_object(bill_id, Bill)
    if not user.admin and user.user_id != bill.user:
        raise ForbiddenException
    transactions = await Transaction.filter(bill_id=bill_id)
    return await json_response(ResponseSchema, transactions, many=True)


@blue.post('/webhook')
async def replenish_bill(request: Request):
    transaction = await validation(request, CreateSchema)
    await get_exists_object(transaction['user_id'], User)
    transaction = await create_transaction(transaction)
    return await json_response(ResponseSchema, transaction)


@blue.delete('/<transaction_id:int>')
async def delete_view(request: Request, transaction_id: int):
    """Удалить товар."""
    if DEBUG:
        raise ForbiddenException
    transaction = await get_exists_object(transaction_id, Transaction)
    await transaction.delete()
    return json('', status=204)
