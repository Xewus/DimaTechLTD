"""Эндпоинты для транзакций.
"""
from sanic import Blueprint, Request
from sanic.response import json
from sanic_ext import validate
from tortoise.exceptions import IntegrityError
from tortoise.transactions import atomic

from src.core.utils import json_response, atomic_execute
from src.db.models import Bill, Transaction, User
from src.schemas.transactions import Createchema, ResponseSchema

blue = Blueprint('transactions', url_prefix='/payment')


@blue.get('/')
async def get_all_transactions(request: Request):
    """Показать все транзакции."""
    transactions = await Transaction.all()
    return await json_response(ResponseSchema, transactions, many=True)


@blue.get('/user/<user_id:int>')
async def get_user_transactions_story(request: Request, user_id: int):
    """Показать транзакции указанного пользователя."""
    transactions = await Transaction.filter(bill__user_id=user_id)
    return await json_response(ResponseSchema, transactions, many=True)


@blue.get('/bill/<bill_id:int>')
async def get_user_transactions_story(request: Request, bill_id: int):
    """Показать транзакции указанного счётв."""
    transactions = await Transaction.filter(bill_id=bill_id)
    return await json_response(ResponseSchema, transactions, many=True)


@atomic
async def fn(*a):
    await a[0].save()
    await a[1].update_or_create()


@atomic
@blue.post('/webhook')
@validate(json=Createchema, body_argument='new_transaction')
async def replenish_bill(request: Request, new_transaction: Createchema):
    if await User.get_or_none(pk=new_transaction.user_id) is None:
        return json({'detail': 'user'})

    try:
        await Bill.update_or_create(
            bill_id=new_transaction.bill_id,
            user_id=new_transaction.user_id,
            balance=new_transaction.amount
        )
        transaction = await Transaction.create(**new_transaction.dict())
    except IntegrityError:
        return json({'detail': 'bd'})
    transaction.user_id = new_transaction.user_id
    print(transaction.__dict__)

    return await json_response(ResponseSchema, transaction)
