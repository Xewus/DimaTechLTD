"""Эндпоинты для счетов.
"""
from sanic import Blueprint, Request
from src.db.models import Bill
from src.schemas.bills import BillCreateSchema, BillResponceSchema
from src.core.utils import json_response

blue = Blueprint('bills', url_prefix='/bills')


@blue.get('/')
async def get_all_bills(request: Request):
    bills = await Bill.all()
    return await json_response(BillResponceSchema, bills, many=True)
