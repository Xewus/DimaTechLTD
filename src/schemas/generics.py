from pydantic import BaseModel, Field, PositiveInt


class UserIdSchema(BaseModel):
    """Схема данных для идентификатора пользователя.

    #### Fields:
    - user_id (PositivInt): Идентификатор пользователя.
    """
    user_id: PositiveInt = Field(
        description='Идентификатор пользователя'
    )


class BillIdSchema(BaseModel):
    """Схема данных для идентификатора счёта.

    #### Fields:
    - bill_id (PositivInt): Идентификатор счёта.
    """
    bill_id: PositiveInt = Field(
        description='Идентификатор счёта'
    )


class ProductIdSchema(BaseModel):
    """Схема данных для идентификатора товара.

    #### Fields:
    - product_id (PositivInt): Идентификатор товара.
    """
    product_id: PositiveInt = Field(
        description='Идентификатор товара'
    )
