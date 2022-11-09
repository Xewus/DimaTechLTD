from pydantic import BaseModel, Field, PositiveInt
from decimal import Decimal

class BillCreateSchema(BaseModel):
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
    user_id: PositiveInt = Field(
        description='`id` владельца счёта'
    )


class BillResponceSchema(BaseModel):
    bill_id: PositiveInt = Field(
        description='`id` счёта'
    )
    balance: Decimal | None = Field(
        description='Баланс счёта'
    )
    user_id: PositiveInt = Field(
        description='`id` владельца счёта'
    )
