from sqlalchemy.orm import Session

from app.application.document.document_service import DocumentService
from app.application.ingestion.embedding_service import EmbeddingService
from app.application.ingestion.ingestion_service import IngestionService
from app.infrastructure.repositories.document_repository import DocumentRepository
from app.infrastructure.vector.pgvector_repository import PgVectorRepository


def get_document_service(db: Session) -> DocumentService:
    return DocumentService(DocumentRepository(db))


def get_embedding_service(db: Session) -> EmbeddingService:
    return EmbeddingService(PgVectorRepository(db))


def get_ingestion_service(db: Session) -> IngestionService:
    embedding_service = get_embedding_service(db)

    return IngestionService(
        embedding_service=embedding_service,
    )