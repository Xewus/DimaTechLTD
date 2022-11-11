from tortoise.exceptions import ValidationError
from tortoise.validators import Validator


class PositiveNumberlValidator(Validator):
    """Допускает только положительные значения.
    """
    def __init__(self, wirh_zero: bool = False) -> None:
        super().__init__()
        self.with_zero = wirh_zero

    def __call__(self, num: int | float):
        if not num > int(self.with_zero):
            raise ValidationError('Value is not %s positive' % num)
