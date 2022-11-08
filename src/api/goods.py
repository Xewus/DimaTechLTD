"""Эндпоинты для товаров.
"""
from sanic import Blueprint, Request
from sanic.response import json, HTTPResponse
from sanic.views import HTTPMethodView

blue = Blueprint('goods', url_prefix='/goods')


class GoodsBuyView(HTTPMethodView):
    """Покупка указанного товара.

    #### Methods:
    - GET:
        Купить товар с указанным `good_id`.
    """
    async def get(self, request: Request, good_id: int) -> HTTPResponse:
        return json({good_id: 'buied'})


class GoodsListView(HTTPMethodView):
    """Просмотр товаров и редактирование товара.

    #### Methods:
    - GET:
        Если переда `good_id`, показать указанный товар.
        Иначе показать весь список товаров.
    - POST:
        Добавить новый товар.
    - PATCH:
        Изменить указанный товар.
    - DELETE:
        Удалить указанный товар.
    """
    async def get(self, request: Request, good_id: int | None = None) -> HTTPResponse:
        if good_id is not None:
            return json({'good': good_id})
        return json(['good1', 'good2'])
    
    async def post(self, request: Request) -> HTTPResponse:
        return json({'good': request.args})
    
    async def patch(self, request: Request, good_id: int) -> HTTPResponse:
        return json({good_id: request.args})
    
    async def delete(self, request: Request, good_id: int) -> HTTPResponse:
        return json({good_id: request.args})


blue.add_route(
    handler=GoodsBuyView.as_view(),
    uri='/buy/<good_id:int>',
    methods=['GET']
)

# Warning: [DEPRECATION v23.3]
# Duplicate route names detected: SanicApp.goods.GoodsListView.
# In the future, Sanic will enforce uniqueness in route naming.
blue.add_route(
    handler=GoodsListView.as_view(),
    uri='/',
    methods=['GET']
)
blue.add_route(
    handler=GoodsListView.as_view(),
    uri='/<good_id:int>',
    methods=['GET', 'PATCH', 'POST', 'DELETE']
)
