from decimal import Decimal

from pydantic import BaseModel, Field, PositiveInt

from .generics import BillIdSchema, UserIdSchema


class ResponseSchema(UserIdSchema, BillIdSchema):
    """Схема данных для ответа.

    #### Fields:
    - user_id (PositivInt): Идентификатор пользователя.
    - bill_id (PositivInt): Идентификатор счёта.
    - balance (Decimal): Баланс счёта.
    """
    balance: Decimal = Field(
        description='Баланс счёта',
        max_digits=12,
        decimal_places=2
    )

    class Config:
        orm_mode = True


class UpdateSchema(BaseModel):
    """Схема данных для обновления счёта.

    #### Fields:
    - balance (Decimal): Баланс счёта.
    """
    balance: Decimal = Field(
        description='Баланс счёта',
        max_digits=12,
        decimal_places=2
    )


class CreateSchema(UserIdSchema):
    """Схема данных для создания счёта.

    #### Fields:
    - user_id (PositivInt): Идентификатор пользователя.
    - bill_id (PositivInt | None): Идентификатор счёта.
    """
    bill_id: PositiveInt | None = Field(
        description='`id` счёта',
        default=None
    )
