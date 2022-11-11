from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from sanic import Request
from tortoise.models import Model

from src.core.exceptions import BadRequestException


async def validation(
    request: Request, model: BaseModel, exclude_none: bool = True
) -> dict:
    '''Проверить входные данныес помощью `pydantic`.'''
    try:
        body: BaseModel = model(**dict(request.json))
    except ValidationError as err:
        raise BadRequestException(err.errors())
    return body.dict(exclude_none=exclude_none)


async def get_exists_object(id: int, model: Model) -> Model:
    obj = await model.get_or_none(pk=id)
    if obj is None:
        raise BadRequestException(
            '%s with id=%d doesnt exists' % (model.__name__, id)
        )
    return obj
