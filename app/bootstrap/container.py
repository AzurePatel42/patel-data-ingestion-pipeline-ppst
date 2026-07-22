from app.infrastructure.repositories.document_repository import DocumentRepository
from app.application.document.document_service import DocumentService

from sqlalchemy.orm import Session
from app.infrastructure.vector.pgvector_repository import PgVectorRepository
from app.application.ingestion.embedding_service import EmbeddingService

def get_document_service(db: Session) -> DocumentService:
    repository = DocumentRepository(db)
    return DocumentService(repository)

def get_embedding_service(db: Session) -> EmbeddingService:
    repository = PgVectorRepository(db)
    return EmbeddingService(repository)