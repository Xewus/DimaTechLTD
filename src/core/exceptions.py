from http import HTTPStatus

from sanic.exceptions import SanicException


class BadRequestException(SanicException):
    def __init__(
        self,
        message: str | bytes | None = None,
        status_code: int = HTTPStatus.BAD_REQUEST
    ) -> None:
        super().__init__(message=message, status_code=status_code)


class ForbiddenException(BadRequestException):
    def __init__(
        self,
        message: str | bytes = 'Forbidden',
    ) -> None:
        super().__init__(message=message, status_code=HTTPStatus.FORBIDDEN)
