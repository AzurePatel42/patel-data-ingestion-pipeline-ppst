from app.application.ingestion.embedding_service import EmbeddingService
from app.application.ingestion.providers.openai_provider import OpenAIEmbeddingProvider
from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.routes.document_routes import router as document_router
from app.core.handlers import register_exception_handlers
from app.infrastructure.db.session import engine
from app.infrastructure.db.models import Base
from app.infrastructure.logging.middleware import LoggingMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME
    )
    
    Base.metadata.create_all(bind=engine)

    app.add_middleware(LoggingMiddleware)

    register_exception_handlers(app)
    
    
    provider = OpenAIEmbeddingProvider()

    embedding_service = EmbeddingService(provider)

    @app.get("/health")
    def health():
        return {"status": "ok"} 
    app.include_router(document_router)

    return app