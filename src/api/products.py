"""Эндпоинты для товаров.
"""
from sanic import Blueprint, Request, json
from sanic_jwt.decorators import inject_user, protected

from src.core.decorators import admin_only
from src.core.exceptions import BadRequestException
from src.core.responses import json_pydantic
from src.db.crud import create, get_exists_object, make_deal, update_object
from src.db.models import Bill, Product, MyUser as User
from src.schemas.products import (BuySchema, CreateSchema, ResponseSchema,
                                  UpdateSchema)
from src.schemas.validators import validation

blue = Blueprint('poducts', url_prefix='/products')


@blue.patch('/buy')
@inject_user()
@protected()
async def buy_view(request: Request, user: User):
    """Купить товар. Можно реализовать покупку разных товаров.

    #### Example:
    '{
        "bill_id":123456,
        "product_id":3,
        "amount":2
    }'
    """
    buy = await validation(request, BuySchema)
    product: Product = await get_exists_object(buy['product_id'], Product)
    bill: Bill = await get_exists_object(buy['bill_id'], Bill)

    if bill.user_id != user.user_id != bill.user:
        raise BadRequestException('Not bill owner')

    await make_deal(product, bill, buy)
    # Показать пользователю количество купленного товара.
    product.amount = buy['amount']
    return await json_pydantic(ResponseSchema, product)


@blue.get('/')
async def get_all_view(request: Request):
    """Показать все товары.
    """
    goods = await Product.all()
    return await json_pydantic(ResponseSchema, goods, many=True)


@blue.get('/<product_id:int>')
async def get_one_view(request: Request, product_id: int):
    """Показать товар c указанным `ID`.
    """
    product = await get_exists_object(product_id, Product)
    return await json_pydantic(ResponseSchema, product)


@blue.post('/')
@inject_user()
@protected()
@admin_only
async def create_view(request: Request):
    """Добавить новый товар.

    #### Example:
    '{
        "name":"Phone",
        "description":"Really cool phone",
        "price":599.99,
        "amount":500
    }'
    """
    product = await validation(request, CreateSchema)
    product = await create(product, Product)
    return await json_pydantic(ResponseSchema, product)


@blue.patch('/<product_id:int>')
@inject_user()
@protected()
@admin_only
async def update_view(
    request: Request, product_id: int, update_data: UpdateSchema
):
    """Изменить товар c указанным `ID`.
    """
    product = await get_exists_object(product_id, Product)
    update_data = await validation(request, UpdateSchema)
    await update_object(product, update_data, Product)
    return await json_pydantic(ResponseSchema, product)


@blue.delete('/<product_id:int>')
@inject_user()
@protected()
@admin_only
async def delete_view(request: Request, product_id: int):
    """Удалить товар c указанным `ID`.
    """
    product = await get_exists_object(product_id, Product)
    await product.delete()
    return json('', status=204)
