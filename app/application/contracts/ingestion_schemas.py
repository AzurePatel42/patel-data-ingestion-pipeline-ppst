from pydantic import BaseModel, Field

class IngestRequest(BaseModel):
    document_id: int
    text: str = Field(..., min_length=1)


class IngestResponse(BaseModel):
    vectors_created: int