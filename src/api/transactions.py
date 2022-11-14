"""Эндпоинты для транзакций.
"""
from sanic import Blueprint, Request
from sanic.response import json
from sanic_jwt.decorators import inject_user, protected

from src.core.decorators import admin_only, admin_or_owner_only
from src.core.exceptions import ForbiddenException
from src.core.responses import json_pydantic
from src.db.crud import create_transaction, get_exists_object
from src.db.models import Bill, Transaction,MyUser as User
from src.schemas.transactions import CreateSchema, ResponseSchema
from src.schemas.validators import validation
from src.settings import AppSettings
blue = Blueprint('payments', url_prefix='/payment')


@blue.get('/')
@inject_user()
@protected()
@admin_only
async def get_all_view(request: Request):
    """Показать все транзакции.
    """
    transactions = await Transaction.all()
    return await json_pydantic(ResponseSchema, transactions, many=True)


@blue.get('/<transaction_id:int>')
@inject_user()
@protected()
async def get_one_view(request: Request, user: User, transaction_id: int):
    """Показать транзакцию c указанным `ID`.
    """
    transaction = await get_exists_object(transaction_id, Transaction)

    if not user.admin and user.user_id != user.pk:
        raise ForbiddenException

    return await json_pydantic(ResponseSchema, transaction)


@blue.get('/user/<user_id:int>')
@inject_user()
@protected()
@admin_or_owner_only
async def get_user_transactions(request: Request, user: User, user_id: int):
    """Показать транзакции пользователя c указанным `ID`.
    """
    if user.admin and user.pk != user_id:
        await get_exists_object(user_id, User)

    transactions = await Transaction.filter(user_id=user_id)
    return await json_pydantic(ResponseSchema, transactions, many=True)


@blue.get('/bill/<bill_id:int>')
@inject_user()
@protected()
async def get_bill_transactions(request: Request, user: User, bill_id: int):
    """Показать транзакции счетов c указанным `ID`.
    """
    bill: Bill = await get_exists_object(bill_id, Bill)

    if not user.admin and user.user_id != bill.user:
        raise ForbiddenException

    transactions = await Transaction.filter(bill_id=bill_id)
    return await json_pydantic(ResponseSchema, transactions, many=True)


@blue.post('/webhook')
async def replenish_bill(request: Request):
    """Принять и обработать транзакцию.

    #### Example:
    '{
        "signature":"70e224ace9d3859aca84ffb88edf593acec92dbb",
        "transaction_id":1234567,
        "user_id":1,
        "bill_id":123456,
        "amount":100
    }'
    """
    transaction = await validation(request, CreateSchema)
    await get_exists_object(transaction['user_id'], User)
    transaction = await create_transaction(transaction)
    return await json_pydantic(ResponseSchema, transaction)


@blue.delete('/<transaction_id:int>')
async def delete_view(request: Request, transaction_id: int):
    """Удалить транзакцию c указанным `ID`.
    """
    if not AppSettings.DEBUG:
        raise ForbiddenException

    transaction = await get_exists_object(transaction_id, Transaction)
    await transaction.delete()
    return json('', status=204)
