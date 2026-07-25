from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.vector.entities import VectorDocument
from app.domain.vector.repository import VectorRepository
from app.infrastructure.vector.models import VectorDocumentModel


class PgVectorRepository(VectorRepository):
    """
    PostgreSQL + pgvector implementation of the VectorRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def save(self, vector_document: VectorDocument) -> None:
        """
        Persist a single vector document.
        """

        model = self._to_model(vector_document)

        try:
            self.db.add(model)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
        

    def save_all(
        self,
        vector_documents: list[VectorDocument],
    ) -> None:
        """
        Persist multiple vector documents in a single transaction.
        """

        if not vector_documents:
            return

        models = [
            self._to_model(vector_document)
            for vector_document in vector_documents
        ]


        try:
            self.db.add_all(models)
            self.db.commit()
            
        except Exception:
            self.db.rollback()
            raise

    def get_by_id(
        self,
        vector_id: UUID,
    ) -> VectorDocument | None:
        """
        Retrieve a vector document by its ID.
        """

        model = self.db.get(VectorDocumentModel, vector_id)

        if model is None:
            return None

        return self._to_entity(model)

    def delete(
        self,
        vector_id: UUID,
    ) -> None:
        """
        Delete a stored vector document.
        """

        model = self.db.get(VectorDocumentModel, vector_id)

        if model is None:
            return

        self.db.delete(model)
        self.db.commit()

    def similarity_search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[VectorDocument]:
        """
        Perform semantic similarity search using pgvector.

        Requires the VectorDocumentModel.embedding column to use
        pgvector.Vector and support the cosine_distance() operator.
        """

        statement = (
            select(VectorDocumentModel)
            .order_by(
                VectorDocumentModel.embedding.cosine_distance(embedding)
            )
            .limit(top_k)
        )

        results = self.db.execute(statement).scalars().all()

        return [
            self._to_entity(model)
            for model in results
        ]

    @staticmethod
    def _to_model(
        vector_document: VectorDocument,
    ) -> VectorDocumentModel:
        """
        Convert a domain entity into a SQLAlchemy model.
        """

        return VectorDocumentModel(
            id=vector_document.id,
            document_id=vector_document.document_id,
            chunk_index=vector_document.chunk_index,
            content=vector_document.content,
            embedding=vector_document.embedding,
            embedding_model=vector_document.embedding_model,
            created_at=vector_document.created_at,
        )

    @staticmethod
    def _to_entity(
        model: VectorDocumentModel,
    ) -> VectorDocument:
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