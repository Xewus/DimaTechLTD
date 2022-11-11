from pydantic import BaseModel, Field, PositiveInt


class UserIdSchema(BaseModel):
    user_id: PositiveInt = Field(
        description='Идентификатор пользователя'
    )


class BillIdSchema(BaseModel):
    bill_id: PositiveInt = Field(
        description='Идентификатор счёта'
    )


class ProductIdSchema(BaseModel):
    product_id: PositiveInt = Field(
        description='Идентификатор товара'
    )
