"""统一异常处理器：集中处理 HTTPException 和未捕获异常。"""
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("backend.exceptions")


class APIError(Exception):
    """业务异常基类，带 HTTP 状态码和可读信息。"""

    def __init__(self, status_code: int = 400, detail: str = "Bad Request"):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def register_exception_handlers(app: FastAPI) -> None:
    """注册所有统一异常处理器。"""

    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": "请求参数校验失败", "errors": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(status_code=500, content={"detail": "服务器内部错误"})
