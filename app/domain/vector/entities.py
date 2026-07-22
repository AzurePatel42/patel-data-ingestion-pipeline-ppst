from dataclasses import dataclass
from typing import List
from uuid import UUID
from datetime import datetime


@dataclass
class VectorDocument:
    """
    Domain entity representing a vectorized document chunk.
    """

    id: UUID
    document_id: UUID
    chunk_index: int
    content: str
    embedding: List[float]
    embedding_model: str
    created_at: datetime