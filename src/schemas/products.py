from decimal import Decimal

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt

from .generics import BillIdSchema, ProductIdSchema


class BuySchema(BillIdSchema, ProductIdSchema):
    """Схема данных для покупки товара.

    #### Fields:
    - bill_id (PositivInt): Идентификатор счёта.
    - product_id (PositivInt): Идентификатор товара.
    - amount (PositiveInt | None): Количество товара.
    """
    amount: PositiveInt | None = Field(
        description='Количество товара',
        default=1
    )


class CreateSchema(BaseModel):
    """Схема данных для создания товара.

    #### Fields:
    - name (str): Название товара.
    - description (str) Описание товара.
    - price (Decimal): Цена товара.
    - amount (NonNegativeInt): Количество товара.
    """
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


class UpdateSchema(BillIdSchema):
    """Схема данных для изменения товара.

    #### Fields:
    - name (str | None): Название товара.
    - description (str | None) Описание товара.
    - price (Decimal | None): Цена товара.
    - amount (NonNegativeInt | None): Количество товара.
    """
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


class ResponseSchema(ProductIdSchema, CreateSchema):
    """Схема данных для идентификатора товара.

    #### Fields:
    - product_id (PositivInt): Идентификатор товара.
    - name (str): Название товара.
    - description (str) Описание товара.
    - price (Decimal): Цена товара.
    - amount (NonNegativeInt): Количество товара.
    """
    class Config:
        orm_mode = True
