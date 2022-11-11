from http import HTTPStatus

from sanic.exceptions import SanicException


class BadRequestException(SanicException):
    def __init__(
        self,
        message: str | bytes | None = None,
        status_code: int = HTTPStatus.BAD_REQUEST,
        quiet: bool | None = None,
        context: dict | None = None,
        extra: dict | None = None
    ) -> None:
        super().__init__(message, status_code, quiet, context, extra)
