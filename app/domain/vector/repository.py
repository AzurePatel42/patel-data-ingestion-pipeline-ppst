from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.domain.vector.entities import VectorDocument


class VectorRepository(ABC):
    """
    Contract for vector storage implementations.
    """

    @abstractmethod
    def save(self, vector_document: VectorDocument) -> None:
        """
        Persist a vector document.
        """
        pass

    @abstractmethod
    def get_by_id(self, vector_id: UUID) -> VectorDocument | None:
        """
        Retrieve a vector document by its ID.
        """
        pass

    @abstractmethod
    def delete(self, vector_id: UUID) -> None:
        """
        Delete a vector document.
        """
        pass

    @abstractmethod
    def similarity_search(
        self,
        embedding: List[float],
        top_k: int = 5,
    ) -> List[VectorDocument]:
        """
        Return the most similar vector documents.
        """
        pass