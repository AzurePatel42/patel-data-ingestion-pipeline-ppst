from pydantic import BaseModel
from app.domain.document.document_status import DocumentStatus

class DocumentCreateRequest(BaseModel):
    filename: str


class DocumentUpdateRequest(BaseModel):
    filename: str | None = None


class DocumentResponse(BaseModel):
    id: int
    filename: str
    status: DocumentStatus
