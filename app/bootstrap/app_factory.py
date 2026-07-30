from fastapi import FastAPI

from app.api.v1.routes.document_routes import router as document_router
from app.bootstrap.database import initialize_database
from app.core.config import settings
from app.core.handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.infrastructure.logging.middleware import LoggingMiddleware


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    # Configure application logging
    configure_logging()

    # Create FastAPI application
    app = FastAPI(
        title=settings.APP_NAME,
    )

    # Initialize database
    initialize_database()

    # Register middleware
    app.add_middleware(LoggingMiddleware)

    # Register global exception handlers
    register_exception_handlers(app)

    # Health endpoint
    @app.get(
        "/health",
        tags=["Health"],
    )
    def health():
        return {"status": "ok"}

    # Register API routes
    app.include_router(document_router)

    return app