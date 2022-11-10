from decimal import Decimal

from pydantic import Field, PositiveInt

from .generics import BillIdSchema, UserIdSchema


class ResponseSchema(UserIdSchema, BillIdSchema):
    balance: Decimal = Field(
        description='Баланс счёта',
        max_digits=12,
        decimal_places=2
    )


class UpdateSchema(BillIdSchema):
    balance: Decimal | None = Field(
        description='Баланс счёта',
        default=.0,
        max_digits=12,
        decimal_places=2
    )


class CreateSchema(UserIdSchema, UpdateSchema):
    bill_id: PositiveInt | None = Field(
        description='`id` счёта',
        default=None
    )

