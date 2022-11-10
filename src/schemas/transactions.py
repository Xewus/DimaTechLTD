from hashlib import sha1

from pydantic import PositiveInt, ValidationError, root_validator

from src.settings import APP_KEY

from .generics import BillIdSchema, UserIdSchema


class StorySchema(UserIdSchema):
    bill_id: PositiveInt | None = None


class ResponseSchema(BillIdSchema, StorySchema):
    signature: str | None = None
    transaction_id: PositiveInt
    amount: PositiveInt

    @root_validator
    def validate_signature(cls, values: dict) -> dict:
        sign = sha1()
        sign.update(
            f"{APP_KEY}:{values['transaction_id']}:{values['user_id']}:"
            f"{values['bill_id']}:{values['amount']}".encode()
        )
        values['signature'] = sign.hexdigest()           
        return values

class Createchema(ResponseSchema):
    signature: str

    @root_validator
    def validate_signature(cls, values: dict) -> dict:
        sign = sha1()
        s = f"{APP_KEY}:{values['transaction_id']}:{values['user_id']}:{values['bill_id']}:{values['amount']}".encode()
        sign.update(s)
        if sign.hexdigest() != values['signature']:
            raise ValidationError('Сигнатура не соответсвует данным')
        return values
