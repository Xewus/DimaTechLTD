from pydantic import Field, PositiveInt, root_validator

from src.core.exceptions import BadRequestException
from src.core.utils import make_signature

from .generics import BillIdSchema, UserIdSchema


class ResponseSchema(UserIdSchema, BillIdSchema):
    """Схема данных для ответа.

    #### Fields:
    - user_id (PositivInt): Идентификатор пользователя.
    - bill_id (PositivInt): Идентификатор счёта.
    - transaction_id (PositiveInt): Идентификатор транзакции.
    - signature (str): Сигнатура транзакции.
    - amount (PositiveInt): Сумма денег в транзакции.
    """
    transaction_id: PositiveInt = Field(
        description='Идентификатор транзакции'
    )
    signature: str = Field(
        description='Сигнатура транзакции'
    )
    amount: PositiveInt = Field(
        description='Сумма денег в транзакции'
    )

    class Config:
        orm_mode = True


class CreateSchema(ResponseSchema):
    """Схема данных для создания транзакции.

    #### Fields:
    - user_id (PositivInt): Идентификатор пользователя.
    - bill_id (PositivInt): Идентификатор счёта.
    - transaction_id (PositiveInt): Идентификатор транзакции.
    - signature (str): Сигнатура транзакции.
    - amount (PositiveInt): Сумма денег в транзакции.
    """
    class Config:
        orm_mode = False

    @root_validator
    def validate_signature(cls, values: dict) -> dict:
        """Проверить данные на соответствие сигнатуре.
        """
        signature = make_signature(values)
        if signature != values['signature']:
            raise BadRequestException('signature')
        return values
