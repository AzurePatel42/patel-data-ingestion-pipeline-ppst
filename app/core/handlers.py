import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AppException,
    NotFoundException,
    ValidationException,
    EmbeddingProviderException,
    StorageException,
)

logger = logging.getLogger(__name__)


def error_response(
    status_code: int,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": str(exc),
            },
        },
    )


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(
        request: Request,
        exc: NotFoundException,
    ):
        logger.warning(
            "NotFoundException [%s] - %s",
            request.url.path,
            exc.message,
        )

        return error_response(404, exc)

    @app.exception_handler(ValidationException)
    async def validation_exception_handler(
        request: Request,
        exc: ValidationException,
    ):
        logger.warning(
            "ValidationException [%s] - %s",
            request.url.path,
            exc.message,
        )

        return error_response(400, exc)

    @app.exception_handler(EmbeddingProviderException)
    async def embedding_provider_exception_handler(
        request: Request,
        exc: EmbeddingProviderException,
    ):
        logger.exception(
            "EmbeddingProviderException [%s]",
            request.url.path,
        )

        return error_response(502, exc)

    @app.exception_handler(StorageException)
    async def storage_exception_handler(
        request: Request,
        exc: StorageException,
    ):
        logger.exception(
            "StorageException [%s]",
            request.url.path,
        )

        return error_response(500, exc)

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):
        logger.exception(
            "AppException [%s]",
            request.url.path,
        )

        return error_response(500, exc)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            "Unhandled exception [%s]",
            request.url.path,
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "type": "InternalServerError",
                    "message": "An unexpected error occurred.",
                },
            },
        )