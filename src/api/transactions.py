"""Эндпоинты для транзакций.
"""
from sanic import Blueprint, Request
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)
from tortoise.exceptions import IntegrityError

from src.core.views import ApiGetMixin, ApiPosMixin
from src.db.models import Bill, Transaction

blue = Blueprint('transactions', url_prefix='transactions')


BillPyd = pydantic_model_creator(Bill)
BillPydList = pydantic_queryset_creator(Bill)


class BillView(ApiGetMixin, ApiPosMixin):
    model = Bill
    one = True
    many = True


class TransactionsView(ApiGetMixin, ApiPosMixin):
    """Обработка платежей.
    """
    model = Transaction
    one = True
    many = True
    
    async def post(self, request: Request) -> HTTPResponse:
        return json({
            'signature': 'f4eae5b2881d8b6a1455f62502d08b2258d80084',
            'transaction_id': 1234567,
            'user_id': 123456,
            'bill_id': 123456,
            'amount': 100
        })


blue.add_route(
    handler=TransactionsView.as_view(),
    uri='/<user_id:int>',
    methods=['GET']
)
blue.add_route(
    handler=TransactionsView.as_view(),
    uri='/',
    methods=['GET', 'PUT']
)
