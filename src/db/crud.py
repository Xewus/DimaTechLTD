"""Функции для работы с данными в БД.
"""
from tortoise.exceptions import IntegrityError
from tortoise.models import Model
from tortoise.transactions import in_transaction

from src.core.exceptions import BadRequestException
from src.core.utils import make_signature
from src.db.models import Bill, Product, Transaction


async def get_exists_object(id: int, model: Model) -> Model:
    """Получить объект из БД.
    """
    obj = await model.get_or_none(pk=id)
    if obj is None:
        raise BadRequestException(
            '%s with id=%d doesnt exists' % (model.__name__, id)
        )
    return obj


async def create(data: dict, model: Model) -> Model:
    """Записать новый объект в БД.
    """
    try:
        obj = await model.create(**data)
    except IntegrityError as err:
        raise BadRequestException(err.args)
    return obj


async def update_object(obj: Model, update_data: dict, model: Model) -> Model:
    """Изменить объект в БД.
    """
    try:
        await obj.update_from_dict(update_data)
    except IntegrityError as err:
        raise BadRequestException(err.args)
    await obj.save()
    return obj


async def make_deal(product: Product, bill: Bill, buy: dict) -> None:
    """Изменить данные в БД согласно проведённой покупки.
    """
    payment = product.price * buy['amount']
    if payment > bill.balance:
        raise BadRequestException('Dont enough money')

    bill.balance -= payment
    product.amount -= buy['amount']
    transaction = Transaction(
        signature=make_signature(buy),
        amount=payment,
        bill_id=bill.bill_id,
        user_id=bill.user_id
    )
    async with in_transaction():
        try:
            await product.save()
            await bill.save()
            await transaction.save()
        except IntegrityError as err:
            raise BadRequestException(err.args)


async def create_transaction(transaction_data: dict) -> Transaction:
    """Изменить баланс счёта и сохранить в истории транзакций.
    """
    bill: Bill = await Bill.get_or_none(pk=transaction_data['bill_id'])
    transaction_data['signature'] = make_signature(transaction_data)

    async with in_transaction():
        try:
            if bill is None:
                await Bill.create(
                    bill_id=transaction_data['bill_id'],
                    user_id=transaction_data['user_id'],
                    balance=transaction_data['amount']
                )
            else:
                bill.balance += transaction_data['amount']
                await bill.save()

            transaction = await Transaction.create(**transaction_data)
        except IntegrityError as err:
            raise BadRequestException(err.args)
    return transaction
