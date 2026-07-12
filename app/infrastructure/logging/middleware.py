import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.infrastructure.logging.logger import get_logger

logger = get_logger("http")


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        logger.info(f"START {request.method} {request.url}")

        try:
            response = await call_next(request)
            duration = time.time() - start_time

            logger.info(
                f"END {request.method} {request.url} "
                f"STATUS={response.status_code} TIME={duration:.4f}s"
            )

            return response

        except Exception as e:
            duration = time.time() - start_time

            logger.error(
                f"ERROR {request.method} {request.url} "
                f"TIME={duration:.4f}s ERROR={str(e)}"
            )
            raise