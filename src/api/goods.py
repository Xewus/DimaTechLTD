"""Эндпоинты для товаров.
"""
from sanic import Blueprint, Request, json
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)
from src.db.models import Good
from src.generics.views import ApiGetMixin, ApiPosMixin, ApiPatchMixin, ApiDeleteMixin

blue = Blueprint('goods', url_prefix='/goods')

GoodPyd = pydantic_model_creator(Good)
GoodPydList = pydantic_queryset_creator(Good)


class GoodsBuyView(HTTPMethodView):
    """Покупка указанного товара.
    """
    async def patch(self, request: Request, pk: int, amount: int = 1) -> HTTPResponse:
        good = await Good.get_or_none(pk=pk)
        amount = dict(request.json).get('amount', 1)
        if good is None or amount < 1 or good.amount < amount:
            return json({'detail': request.json}, status=422)
        good.amount -= amount
        await good.save()
        good = await GoodPyd.from_tortoise_orm(good)
        return json(good.dict())


class GoodsView(ApiGetMixin, ApiPosMixin, ApiPatchMixin, ApiDeleteMixin):
    model = Good
    one = True
    many = True


blue.add_route(
    handler=GoodsBuyView.as_view(),
    uri='/buy/<pk:int>',
    methods=['PATCH']
)


blue.add_route(
    handler=GoodsView.as_view(),
    uri='/',
    methods=['GET']
)
blue.add_route(
    handler=GoodsView.as_view(),
    uri='/<pk:int>',
    methods=['GET', 'PATCH', 'POST', 'DELETE']
)
