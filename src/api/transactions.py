"""Эндпоинты для транзакций.
"""
from sanic import Blueprint, Request
from sanic.response import json

from src.core.views import json_response
from src.db.crud import create_transaction
from src.db.models import Bill, Transaction, User
from src.schemas.transactions import CreateSchema, ResponseSchema
from src.schemas.validators import get_exists_object, validation

blue = Blueprint('transactions', url_prefix='/payment')


@blue.get('/')
async def get_all_view(request: Request):
    """Показать все транзакции."""
    transactions = await Transaction.all()
    return await json_response(ResponseSchema, transactions, many=True)


@blue.get('/<transaction_id:int>')
async def get_one_view(request: Request, transaction_id: int):
    """Показать указанного транзакцию."""
    transaction = await get_exists_object(transaction_id, Transaction)
    return await json_response(ResponseSchema, transaction)


@blue.get('/user/<user_id:int>')
async def get_user_transactions(request: Request, user_id: int):
    """Показать транзакции указанного пользователя."""
    await get_exists_object(user_id, User)
    transactions = await Transaction.filter(user_id=user_id)
    return await json_response(ResponseSchema, transactions, many=True)


@blue.get('/bill/<bill_id:int>')
async def get_bill_transactions(request: Request, bill_id: int):
    """Показать транзакции указанного счётв."""
    await get_exists_object(bill_id, Bill)
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
    transaction = await get_exists_object(transaction_id, Transaction)
    await transaction.delete()
    return json('', status=204)
