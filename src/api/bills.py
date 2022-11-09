"""Эндпоинты для счетов.
"""
from sanic import Blueprint, Request
from sanic.response import json
from sanic_ext import validate
from tortoise.exceptions import IntegrityError

from src.core.utils import json_response
from src.db.models import Bill
from src.schemas.bills import (BillCreateSchema, BillResponseSchema,
                               BillUpdateSchema)

blue = Blueprint('bills', url_prefix='/bills')


@blue.get('/')
async def get_all_bills(request: Request):
    bills = await Bill.all()
    return await json_response(BillResponseSchema, bills, many=True)


@blue.get('/<bill_id:int>')
async def get_bill(request: Request, bill_id: int):
    bill: Bill = await Bill.get_or_none(pk=bill_id)
    if bill is None:
        return json({'detail': 'bill'}, status=422)
    return await json_response(BillResponseSchema, bill)


@blue.get('/my/<user_id:int>')
async def get_my_bills(request: Request, user_id: int):
    bills = await Bill.filter(user_id=user_id)
    return await json_response(BillResponseSchema, bills, many=True)



@blue.post('/')
@validate(json=BillCreateSchema, body_argument='new_good')
async def create_good(request: Request, new_good: BillCreateSchema):
    bill = new_good.dict(exclude_none=True)
    try:
        bill = await Bill.create(**bill)
    except IntegrityError:
        return json({'detail': 'bill'}, status=422)
    return await json_response(BillResponseSchema, bill)


@blue.patch('/<bill_id:int>')
@validate(json=BillUpdateSchema, body_argument='update_data')
async def update_user(request: Request, bill_id: int, update_data: BillUpdateSchema):
    bill: Bill = await Bill.get_or_none(pk=bill_id)
    if bill is None:
        return json({'detail': 'bill'}, status=422)
    bill.update_from_dict(update_data.dict(exclude_none=True))
    await bill.save()
    return await json_response(BillResponseSchema, bill)
