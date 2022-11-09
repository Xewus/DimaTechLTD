from sanic import json
from sanic.response import HTTPResponse
from pydantic import BaseModel as PydanticModel
from tortoise.queryset import QuerySetSingle, QuerySet

async def json_response(
    schema: PydanticModel,
    queryset: QuerySet | QuerySetSingle,
    many: bool = False
) -> HTTPResponse:
    if not many:
        return json(schema(**queryset.__dict__).dict())
    return json([schema(**obj.__dict__).dict() for obj in queryset])
