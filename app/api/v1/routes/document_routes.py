from fastapi import APIRouter, Depends, HTTPException

from app.bootstrap.container import get_document_service
from sqlalchemy.orm import Session

from app.application.contracts.document_schemas import DocumentCreateRequest, DocumentResponse,  DocumentUpdateRequest

from app.bootstrap.container import get_document_service
from app.infrastructure.db.deps import get_db

from app.bootstrap.container import get_embedding_service
from app.application.ingestion.embedding_service import EmbeddingService
from app.application.contracts.ingestion_schemas import IngestRequest


router = APIRouter()


@router.post("/documents", response_model=DocumentResponse)
def create_document(payload: DocumentCreateRequest, db = Depends(get_db)):

    service = get_document_service(db)

    document = service.create_document(

        filename=payload.filename
    )

    return document

@router.get("/documents", response_model=list[DocumentResponse])
def get_documents(db = Depends(get_db)):

    service = get_document_service(db)

    return service.get_documents()


@router.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db = Depends(get_db)):

    service = get_document_service(db)

    document = service.get_document(document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

@router.put("/documents/{document_id}", response_model=DocumentResponse)
def update_document(document_id: int, payload: DocumentUpdateRequest, db: Session = Depends(get_db)):

    service = get_document_service(db)

    updated = service.update_document(document_id, payload.model_dump(exclude_unset=True))

    if not updated:
        raise HTTPException(status_code=404, detail="Document not found")

    return updated


@router.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):

    service = get_document_service(db)

    success = service.delete_document(document_id)

    if not success:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted successfully"}

@router.post("/documents/upload", response_model=DocumentResponse)
def upload_document(payload: DocumentCreateRequest, db = Depends(get_db)):

    service = get_document_service(db)

    document = service.create_document(

        filename=payload.filename
    )

    return document

@router.post("/ingest")
def ingest(
    request: IngestRequest,
    db: Session = Depends(get_db),
):

    service = get_embedding_service(db)

    return service.ingest(request)
    