"""Эндпоинты для счетов.
"""
from sanic import Blueprint, Request
from sanic.response import json
from sanic_ext import validate
from tortoise.exceptions import IntegrityError

from src.core.utils import json_response
from src.db.models import Bill, User
from src.schemas.bills import CreateSchema, ResponseSchema, UpdateSchema

blue = Blueprint('bills', url_prefix='/bills')


@blue.get('/')
async def get_all_view(request: Request):
    """Показать все счета."""
    bills = await Bill.all()
    return await json_response(ResponseSchema, bills, many=True)


@blue.get('/<bill_id:int>')
async def get_one_view(request: Request, bill_id: int):
    """Показать указанный счёт"""
    bill: Bill = await Bill.get_or_none(pk=bill_id)
    if bill is None:
        return json({'detail': 'bill'}, status=422)
    return await json_response(ResponseSchema, bill)


@blue.get('/user/<user_id:int>')
async def get_my_view(request: Request, user_id: int):
    """Показать счета указанного пользователя"""
    bills = await Bill.filter(user_id=user_id)
    return await json_response(ResponseSchema, bills, many=True)


@blue.post('/')
@validate(json=CreateSchema, body_argument='new_bill')
async def create_view(request: Request, new_bill: CreateSchema):
    """Создать новый счёт."""
    bill = new_bill.dict(exclude_none=True)
    user = await User.get_or_none(pk=new_bill.user_id)
    if user is None:
        return json({'detail': 'no user'})
    try:
        bill = await Bill.create(**bill)
    except IntegrityError:
        return json({'detail': 'bill'}, status=422)
    return await json_response(ResponseSchema, bill)


@blue.patch('/')
@validate(json=UpdateSchema, body_argument='update_data')
async def update_view(request: Request, bill_id: int, update_data: UpdateSchema):
    """Изменить счёт."""
    bill: Bill = await Bill.get_or_none(pk=update_data.bill_id)
    if bill is None:
        return json({'detail': 'bill'}, status=422)
    bill.update_from_dict(update_data.dict(exclude_none=True))
    await bill.save()
    return await json_response(ResponseSchema, bill)
