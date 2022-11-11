from hashlib import sha1

from src.settings import APP_KEY


def make_signature(values: dict) -> str:
    sign = sha1()
    sign.update(
        f"{APP_KEY}:{values['transaction_id']}:{values['user_id']}"
        f":{values['bill_id']}:{values['amount']}".encode()
    )
    return sign.hexdigest()
