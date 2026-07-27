from pydantic import BaseModel

from app.domain.document.document_status import DocumentStatus


class UploadResponse(BaseModel):
    document_id: int
    filename: str
    status: DocumentStatus
    vectors_created: int