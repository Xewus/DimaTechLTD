from pydantic import BaseModel as PydanticModel
from sanic import json
from sanic.response import HTTPResponse
from tortoise.queryset import QuerySet, QuerySetSingle


async def json_response(
    schema: PydanticModel,
    queryset: QuerySet | QuerySetSingle,
    many: bool = False
) -> HTTPResponse:
    if not many:
        return json(schema.from_orm(queryset).dict())
    return json([schema.from_orm(obj).dict() for obj in queryset])
