from hashlib import sha1

from src.core.exceptions import BadRequestException
from src.settings import APP_KEY


def make_signature(values: dict) -> str:
    sign = sha1()
    sign.update(
        f"{APP_KEY}:{values['bill_id']}:{values['amount']}".encode()
    )
    return sign.hexdigest()
