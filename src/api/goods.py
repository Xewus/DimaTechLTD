"""Эндпоинты для товаров.
"""
from sanic import Blueprint, Request, json
from sanic_ext import validate
from tortoise.exceptions import IntegrityError

from src.core.utils import json_response, atomic_execute
from src.db.models import Bill, Good
from src.schemas.goods import (BuySchema, CreateSchema, ResponseSchema,
                               UpdateSchema)

blue = Blueprint('goods', url_prefix='/goods')


@blue.patch('/buy')
@validate(json=BuySchema, body_argument='buy')
async def buy_view(request: Request, buy: BuySchema):
    """Купить товар. Можно реаоизовать покупку разных товаров."""
    good = await Good.get_or_none(pk=buy.good_id)
    if good is None:
        return json({'detail': 'good'}, status=422)
    if good.amount < buy.amount:
        return json({'detail': 'amount'})

    bill = await Bill.get(pk=buy.bill_id)
    payment = good.price * buy.amount
    if payment > bill.balance:
        return json({'detail': 'balance'})
    
    bill.balance -= payment    
    good.amount -= buy.amount
    try:
        await atomic_execute(bill.save, good.save)
    except IntegrityError:
        return json({'detail': 'db'})


    # Показать покупателю количество купленного товара
    good.amount = buy.amount
    return await json_response(ResponseSchema, good)


@blue.get('/')
async def get_all_view(request: Request):
    """Показать все товары."""
    goods = await Good.all()
    return await json_response(ResponseSchema, goods, many=True)


@blue.get('/<good_id:int>')
async def get_one_view(request: Request, good_id: int):
    """Показать указанныйтовар."""
    good: Good = await Good.get_or_none(pk=good_id)
    if good is None:
        return json({'detail': 'good'}, status=422)
    return await json_response(ResponseSchema, good)


@blue.post('/')
@validate(json=CreateSchema, body_argument='new_good')
async def create_view(request: Request, new_good: CreateSchema):
    """Добавить новый товар."""
    good = new_good.dict()
    try:
        good = await Good.create(**good)
    except IntegrityError:
        return json({'detail': new_good.username}, status=422)
    return await json_response(ResponseSchema, good)


@blue.patch('/<good_id:int>')
@validate(json=UpdateSchema, body_argument='update_data')
async def update_view(request: Request, good_id: int, update_data: UpdateSchema):
    """Изменить товар"""
    good: Good = await Good.get_or_none(pk=good_id)
    if good is None:
        return json({'detail': 'good'}, status=422)
    good.update_from_dict(update_data.dict(exclude_none=True))
    await good.save()
    return await json_response(ResponseSchema, good)


@blue.delete('/<good_id:int>')
async def delete_view(request: Request, good_id: int):
    """Удалить товар."""
    good: Good = await Good.get_or_none(pk=good_id)
    if good is None:
        return json({'detail': 'error'}, status=422)
    await good.delete()
    return json('', status=204)
