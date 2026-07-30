from sqlalchemy.orm import Session

from app.application.document.document_service import DocumentService
from app.application.ingestion.embedding_service import EmbeddingService
from app.application.ingestion.ingestion_service import IngestionService
from app.application.ingestion.upload_service import UploadService
from app.infrastructure.repositories.document_repository import DocumentRepository
from app.infrastructure.vector.pgvector_repository import PgVectorRepository


def get_document_service(db: Session) -> DocumentService:
    return DocumentService(
        DocumentRepository(db),
    )


def get_embedding_service(db: Session) -> EmbeddingService:
    return EmbeddingService(
        PgVectorRepository(db),
    )


def get_ingestion_service(db: Session) -> IngestionService:
    embedding_service = get_embedding_service(db)

    return IngestionService(
        embedding_service=embedding_service,
    )


def get_upload_service(db: Session) -> UploadService:
    document_service = get_document_service(db)
    ingestion_service = get_ingestion_service(db)

    return UploadService(
        document_service=document_service,
        ingestion_service=ingestion_service,
    )