"""
- `Пользователь` – репрезентация пользователей в приложении.
  Должны быть обычные и админ пользователи.
  Админ  создаётся на старте приложения.
- `Товар` – Состоит из заголовка, описания и цены
- `Счёт` – Имеет идентификатор счёта и баланс.
  Привязан к пользователю. У пользователя может быть несколько счетов.
- `Транзакция` – история зачисления на счёт.
  Хранит сумму зачисления и идентификатор счёта
"""
from __future__ import annotations

from passlib.context import CryptContext
from tortoise import fields
from tortoise.models import Model

from src.db.validators import PositiveNumberlValidator
from src.settings import MAX_LEN_USERNAME

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(Model):
    user_id = fields.BigIntField(pk=True)
    username = fields.CharField(
        max_length=MAX_LEN_USERNAME,
        unique=True,
        description='Юзернейм пользователя'
    )
    hash = fields.CharField(
        max_length=64,
        description='Хэш для аутенфитикации'
    )
    admin = fields.BooleanField(
        default=False,
        description='Являяется ли пользователь админом'
    )
    active = fields.BooleanField(
        default=False,
        description='Активен ли пользователь'
        'Вместо удаления - пользователя следует деактивировать'
    )

    class PydanticMeta:
        exclude = ('hash',)

    def __init__(self, password: str | None, **kwargs) -> None:
        super().__init__(**kwargs)
        if password is not None:
            self.set_hash(password)

    def __str__(self) -> str:
        return f'{self.username}, active: {self.active}, admin: {self.admin}'

    def set_hash(self, password: str) -> None:
        """Вычислить и установить атрибут `hash` объекта.

        #### Args:
        - password (str): Пароль.
        """
        self.hash = pass_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Проверить соответсвие пароля и хэша.

        #### Args:
        - password (str): Проверяемый пароль.

        #### Returns:
        - bool: Правильный ли пароль.
        """
        return pass_context.verify(password, self.hash)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username
        }


class Product(Model):
    product_id = fields.BigIntField(pk=True)
    name = fields.CharField(
        max_length=255,
        unique=True,
        description='Название товара'
    )
    description = fields.TextField(
        description='Описание товара'
    )
    price = fields.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[PositiveNumberlValidator],
        description='Цена товара'
    )
    amount = fields.IntField(
        default=0,
        validators=[PositiveNumberlValidator],
        description='Количество товара'
    )


class Bill(Model):
    bill_id = fields.BigIntField(pk=True)
    balance = fields.DecimalField(
        default=.0,
        max_digits=12,
        decimal_places=2,
        description='Баланс пользователя'
    )
    user = fields.ForeignKeyField(
        model_name='models.User',
        related_name='bills',
        on_delete=fields.RESTRICT,
        description='Владелец счёта. Удаление владельца запрещено.'
    )


class Transaction(Model):
    transaction_id = fields.BigIntField(pk=True)
    transaction_datetime = fields.DatetimeField(
        auto_now_add=True,
        description='Дата и время транзакции'
    )
    signature = fields.CharField(
        description='Сигнатура платежа',
        max_length=64
    )
    amount = fields.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[PositiveNumberlValidator],
        description='Сумма платежа'
    )
    bill = fields.ForeignKeyField(
        model_name='models.Bill',
        related_name='transactions',
        on_delete=fields.RESTRICT,
        description='С каким счёта была проведена тразакция'
    )
    user = fields.ForeignKeyField(
        model_name='models.User',
        related_name='transactions',
        on_delete=fields.RESTRICT,
        description='Владелец счёта. Удаление владельца запрещено.'
    )


async def create_first_user() -> None:
    """Создаёт первого пользователя-админа, если БД пуста.
    """
    user = await User.first()
    if user:
        print(user)
        return None
    try:
        from src.settings import FIRST_USER
        user = await User.create(**FIRST_USER)
        await user.save()
    except ImportError:
        print('В настройках нет данных для первого пользователя')
        return None
