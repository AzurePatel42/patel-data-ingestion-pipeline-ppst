from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.bootstrap.container import (
    get_document_service,
    get_ingestion_service,
    get_upload_service,
)
from app.infrastructure.db.deps import get_db

from app.application.contracts.document_schemas import (
    DocumentCreateRequest,
    DocumentResponse,
)

from app.application.contracts.ingestion_schemas import (
    IngestRequest,
    IngestResponse,
)

from app.application.contracts.upload_schemas import (
    UploadResponse,
)

router = APIRouter(tags=["Documents"])


@router.post(
    "/documents",
    response_model=DocumentResponse,
)
def create_document(
    payload: DocumentCreateRequest,
    db: Session = Depends(get_db),
):
    """
    Create document metadata.
    """
    service = get_document_service(db)

    return service.create_document(
        filename=payload.filename,
    )


@router.get(
    "/documents",
    response_model=List[DocumentResponse],
)
def get_documents(
    db: Session = Depends(get_db),
):
    """
    Retrieve all documents.
    """
    service = get_document_service(db)

    return service.get_documents()


@router.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve a document by its ID.
    """
    service = get_document_service(db)

    return service.get_document(document_id)


@router.delete(
    "/documents/{document_id}",
    status_code=204,
)
def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete a document.
    """
    service = get_document_service(db)

    service.delete_document(document_id)


@router.post(
    "/documents/upload",
    response_model=UploadResponse,
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a document, automatically ingest it,
    generate embeddings, and persist vectors.
    """
    service = get_upload_service(db)

    return service.upload(file)


@router.post(
    "/documents/ingest",
    response_model=IngestResponse,
)
def ingest_document(
    request: IngestRequest,
    db: Session = Depends(get_db),
):
    """
    Ingest raw text into the vector store.
    """
    service = get_ingestion_service(db)

    vectors = service.ingest_text(
        document_id=request.document_id,
        text=request.text,
    )

    return IngestResponse(
        vectors_created=len(vectors),
    )