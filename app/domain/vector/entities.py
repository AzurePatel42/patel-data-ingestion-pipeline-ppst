from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class VectorDocument:
    """
    Domain entity representing a vectorized document chunk.
    """

    id: UUID
    document_id: int
    chunk_index: int
    content: str
    embedding: list[float]
    embedding_model: str
    created_at: datetime