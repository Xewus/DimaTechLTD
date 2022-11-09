from pydantic import BaseModel as PydanticModel
from sanic import json
from sanic.response import HTTPResponse
from tortoise.models import Model
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.transactions import atomic


@atomic()
async def saving_together(*objs: tuple[Model]):
    for obj in objs:
        await obj.save()


async def json_response(
    schema: PydanticModel,
    queryset: QuerySet | QuerySetSingle,
    many: bool = False
) -> HTTPResponse:
    if not many:
        return json(schema(**queryset.__dict__).dict())
    return json([schema(**obj.__dict__).dict() for obj in queryset])
