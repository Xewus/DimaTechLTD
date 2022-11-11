from pydantic import PositiveInt, root_validator

from src.core.exceptions import BadRequestException
from src.core.utils import make_signature

from .generics import BillIdSchema, UserIdSchema


class StorySchema(UserIdSchema):
    bill_id: PositiveInt | None = None


class ResponseSchema(BillIdSchema, StorySchema):
    signature: str
    transaction_id: PositiveInt
    amount: PositiveInt

    class Config:
        orm_mode = True


class CreateSchema(ResponseSchema):
    class Config:
        orm_mode = False

    @root_validator
    def validate_signature(cls, values: dict) -> dict:
        signature = make_signature(values)
        if signature != values['signature']:
            raise BadRequestException('signature')
        return values
