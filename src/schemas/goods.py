from decimal import Decimal

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt


class GoodCreateSchema(BaseModel):
    name: str = Field(    
        description='Название товара',
        max_length=255
    )
    description: str = Field(
        description='Описание товара'
    )
    price: Decimal = Field(
        description='Цена товара',
        default=.01,
        max_digits=12,
        decimal_places=2
    )
    amount: NonNegativeInt = Field(
        description='Количество товара',
        default=0
    )


class GoodBuySchema(BaseModel):
    bill_id: PositiveInt
    good_id: PositiveInt = Field(
        description='id товара'
    )
    amount: PositiveInt = Field(
        description='Количество товара',
        default=1
    )


class GoodUpdateSchema(BaseModel):
    name: str | None = Field(
        description='Название товара',
        default=None,
        max_length=255
    )
    description: str | None = Field(
        description='Описание товара', 
        default=None
    )
    price: Decimal | None = Field(
        description='Цена товара',
        default=None,
        max_digits=12,
        decimal_places=2
    )
    amount: NonNegativeInt | None = Field(
        description='Количество товара', 
        default=None
    )



class GoodResponseSchema(GoodCreateSchema):
    good_id: PositiveInt = Field(
        description='id товара'
    )
