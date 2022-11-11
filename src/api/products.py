"""Эндпоинты для товаров.
"""
from sanic import Blueprint, Request, json

from src.core.views import json_response
from src.db.crud import create, make_deal, update_object
from src.db.models import Bill, Product
from src.schemas.products import (BuySchema, CreateSchema, ResponseSchema,
                                  UpdateSchema)
from src.schemas.validators import get_exists_object, validation

blue = Blueprint('poducts', url_prefix='/products')


@blue.patch('/buy')
async def buy_view(request: Request):
    """Купить товар. Можно реализовать покупку разных товаров."""
    buy = await validation(request, BuySchema)
    product: Product = await get_exists_object(buy['product_id'], Product)
    bill: Bill = await get_exists_object(buy['bill_id'], Bill)
    await make_deal(product, bill, buy)
    product.amount = buy['amount']
    return await json_response(ResponseSchema, product)


@blue.get('/')
async def get_all_view(request: Request):
    """Показать все товары."""
    goods = await Product.all()
    return await json_response(ResponseSchema, goods, many=True)


@blue.get('/<product_id:int>')
async def get_one_view(request: Request, product_id: int):
    """Показать указанныйтовар."""
    product = await get_exists_object(product_id, Product)
    return await json_response(ResponseSchema, product)


@blue.post('/')
async def create_view(request: Request):
    """Добавить новый товар."""
    product = await validation(request, CreateSchema)
    product = await create(product, Product)
    return await json_response(ResponseSchema, product)


@blue.patch('/<product_id:int>')
async def update_view(
    request: Request, product_id: int, update_data: UpdateSchema
):
    """Изменить товар"""
    product = await get_exists_object(product_id, Product)
    update_data = await validation(request, UpdateSchema)
    await update_object(product, update_data, Product)
    return await json_response(ResponseSchema, product)


@blue.delete('/<product_id:int>')
async def delete_view(request: Request, product_id: int):
    """Удалить товар."""
    product = await get_exists_object(product_id, Product)
    await product.delete()
    return json('', status=204)
