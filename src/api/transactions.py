"""Эндпоинты для транзакций.
"""
from sanic import Blueprint, Request
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

blue = Blueprint('transactions', url_prefix='transactions')


class TransactionsView(HTTPMethodView):
    """Обработка платежей.

    #### Methods:
    - GET:
        Если передан `user_id`, показать транзакции указанного пользователя.
        Иначе показать все транзакции.
    - POST:
        Провести новую транзакцию.
    """
    async def get(self, request: Request, user_id: int | None = None) -> HTTPResponse:
        if user_id is not None:
            return json({user_id:[1, 2]})
        return json([1, 2 ,3])
    
    async def put(self, request: Request) -> HTTPResponse:
        return json({
            'signature': 'f4eae5b2881d8b6a1455f62502d08b2258d80084',
            'transaction_id': 1234567,
            'user_id': 123456,
            'bill_id': 123456,
            'amount': 100
        })


# Warning: [DEPRECATION v23.3]
# Duplicate route names detected: SanicApp.transactions.TransactionsView.
# In the future, Sanic will enforce uniqueness in route naming.
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
