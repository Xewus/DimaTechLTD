from typing import Iterable

from sanic import Request, json
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)
from tortoise.exceptions import IntegrityError
from tortoise.models import Model


class BaseView(HTTPMethodView):
    """Баззовый view-класс

    #### AttrsL
    - model (Model): Модель ORM с которой работает класс.
    - one (bool):Вывод одного объекта.
    - many (bool): Вывод спимска объектов.
    """ 
    model: Model = None
    one: bool = False
    many: bool = False

    def __init__(self) -> None:
        if self.model is None:
            raise NotImplementedError('Необходимо подключить модель ORM')
        if self.one:
            self.pydantic_model = pydantic_model_creator(self.model)
        if self.many:
            self.pydantic_list = pydantic_queryset_creator(self.model)
        super().__init__()


class ApiGetMixin(BaseView):
    async def get(self, request: Request, pk: int | None = None) -> HTTPResponse:
        # if pk is not None:
        #     obj = await self.model.get_or_none(pk=pk)
        #     if obj is None:
        #         return json({'detail': request.json}, status=422)
        #     obj = await self.pydantic_model.from_tortoise_orm(obj)
        #     return json(obj.dict())
        
        objs = await self.pydantic_list.from_queryset(self.model.all())
        return json(objs.dict()['__root__'])


class ApiPosMixin(BaseView):
    async def post(self, request: Request) -> HTTPResponse:
        try:
            obj = await self.model.create(**dict(request.json))
        except IntegrityError:
            return json({'detail': request.json}, status=422)
        obj = await self.pydantic_model.from_tortoise_orm(obj)
        return json(obj.dict())


class ApiPatchMixin(BaseView):
    async def patch(self, request: Request, pk: int) -> HTTPResponse:
        obj = await self.model.get_or_none(pk=pk)
        if obj is None:
            return json({'detail': request.json}, status=422)
        obj.update_from_dict(dict(request.json))
        await obj.save()
        obj = await self.pydantic_model.from_tortoise_orm(obj)
        return json(obj.dict())


class ApiDeleteMixin(BaseView):
    async def delete(self, request: Request, pk: int) -> HTTPResponse:
        obj = await self.model.get_or_none(pk=pk)
        if obj is None:
            return json({'detail': request.json}, status=422)
        await obj.delete()
        return json({'detail': 'deleted'}, status=204)
