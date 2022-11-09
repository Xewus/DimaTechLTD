from decimal import Decimal

from pydantic import BaseModel, Field, PositiveInt


class BillUserSchema(BaseModel):
    user_id: PositiveInt = Field(
        description='`id` владельца счёта'
    )

class BillCreateSchema(BillUserSchema):
    bill_id: PositiveInt | None = Field(
        description='`id` счёта',
        default=None
    )
    balance: Decimal | None = Field(
        description='Баланс счёта',
        default=.0,
        max_digits=12,
        decimal_places=2
    )


class BillUpdateSchema(BaseModel):
    balance: Decimal = Field(
        description='Баланс счёта',
        max_digits=12,
        decimal_places=2
    )


class BillResponseSchema(BillUserSchema):
    bill_id: PositiveInt = Field(
        description='`id` счёта'
    )
    balance: Decimal | None = Field(
        description='Баланс счёта'
    )
