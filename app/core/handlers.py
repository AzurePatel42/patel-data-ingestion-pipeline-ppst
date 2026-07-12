from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import NotFoundException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(
        request: Request,
        exc: NotFoundException
    ):
       return JSONResponse(
    status_code=404,
    content={
        "success": False,
        "error": {
            "type": "NotFoundException",
            "message": exc.message
        }
    }
)