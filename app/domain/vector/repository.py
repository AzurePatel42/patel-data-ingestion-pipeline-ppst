from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.vector.entities import VectorDocument


class VectorRepository(ABC):

    """
Repository contract for vector persistence.

The application layer depends on this abstraction,
allowing different vector storage implementations
(pgvector, Pinecone, Qdrant, Weaviate, etc.)
without changing business logic.
"""


    
    @abstractmethod
    def save_all(
        self,
        vector_documents: list[VectorDocument],
    ) -> None:
        """
        Persist multiple vector documents atomically.
        """
        ...

    @abstractmethod
    def similarity_search(
        self,
        embedding: list[float],
        top_k: int,
    ) -> list[VectorDocument]:
        ...

    @abstractmethod
    def get_by_id(
        self,
        vector_id: UUID,
    ) -> VectorDocument | None:
        ...

    @abstractmethod
    def delete(
        self,
        vector_id: UUID,
    ) -> None:
        ...