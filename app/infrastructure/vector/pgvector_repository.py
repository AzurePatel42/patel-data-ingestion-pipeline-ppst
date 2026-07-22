from uuid import UUID

from pgvector.sqlalchemy import cosine_distance
from sqlalchemy.orm import Session

from app.domain.vector.entities import VectorDocument
from app.domain.vector.repository import VectorRepository
from app.infrastructure.vector.models import VectorDocumentModel


class PgVectorRepository(VectorRepository):
    """
    PostgreSQL + pgvector implementation of VectorRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_model(entity: VectorDocument) -> VectorDocumentModel:
        """
        Convert a domain entity into a SQLAlchemy model.
        """
        return VectorDocumentModel(
            id=entity.id,
            document_id=entity.document_id,
            chunk_index=entity.chunk_index,
            content=entity.content,
            embedding=entity.embedding,
            embedding_model=entity.embedding_model,
            created_at=entity.created_at,
        )

    @staticmethod
    def _to_domain(model: VectorDocumentModel) -> VectorDocument:
        """
        Convert a SQLAlchemy model into a domain entity.
        """
        return VectorDocument(
            id=model.id,
            document_id=model.document_id,
            chunk_index=model.chunk_index,
            content=model.content,
            embedding=model.embedding,
            embedding_model=model.embedding_model,
            created_at=model.created_at,
        )

    def save(self, vector_document: VectorDocument) -> None:
        """
        Persist a vector document.
        """
        model = self._to_model(vector_document)

        self.db.add(model)
        self.db.commit()

    def get_by_id(self, vector_id: UUID) -> VectorDocument | None:
        """
        Retrieve a vector document by its ID.
        """
        model = self.db.get(VectorDocumentModel, vector_id)

        if model is None:
            return None

        return self._to_domain(model)

    def delete(self, vector_id: UUID) -> None:
        """
        Delete a vector document.
        """
        model = self.db.get(VectorDocumentModel, vector_id)

        if model is not None:
            self.db.delete(model)
            self.db.commit()

    def similarity_search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[VectorDocument]:
        """
        Return the most similar vector documents using cosine distance.
        """
        models = (
            self.db.query(VectorDocumentModel)
            .order_by(
                cosine_distance(
                    VectorDocumentModel.embedding,
                    embedding,
                )
            )
            .limit(top_k)
            .all()
        )

        return [self._to_domain(model) for model in models]