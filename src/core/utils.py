from pydantic import BaseModel as PydanticModel
from sanic import json
from sanic.response import HTTPResponse
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.transactions import atomic
from typing import Awaitable


@atomic()
async def atomic_execute(*funcs: Awaitable):
    for func in funcs:
        _ = await func()


async def json_response(
    schema: PydanticModel,
    queryset: QuerySet | QuerySetSingle,
    many: bool = False
) -> HTTPResponse:
    if not many:
        return json(schema(**queryset.__dict__).dict())
    return json([schema(**obj.__dict__).dict() for obj in queryset])
