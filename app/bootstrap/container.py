from app.infrastructure.repositories.document_repository import DocumentRepository
from app.application.document.document_service import DocumentService


def get_document_service(db):
    repository = DocumentRepository(db)
    service = DocumentService(repository)
    return service