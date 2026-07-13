from pydantic import BaseModel


class DocumentCreateRequest(BaseModel):
    filename: str


class DocumentUpdateRequest(BaseModel):
    filename: str | None = None


class DocumentResponse(BaseModel):
    id: int
    filename: str
    supported: bool