"""Валидаторы моделей `pydantic`.
"""
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from sanic import Request

from src.core.exceptions import BadRequestException


async def validation(
    request: Request, model: BaseModel, exclude_none: bool = True
) -> dict:
    """Проверить входные данные с помощью `pydantic`.
    """
    try:
        body: BaseModel = model(**dict(request.json))
    except ValidationError as err:
        raise BadRequestException(err.errors())
    return body.dict(exclude_none=exclude_none)
