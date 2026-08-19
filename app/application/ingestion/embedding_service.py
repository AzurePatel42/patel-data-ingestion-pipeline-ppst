from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.application.ingestion.providers.embedding_provider import EmbeddingProvider
from app.application.ingestion.providers.openai_provider import OpenAIEmbeddingProvider
from app.core.exceptions import EmbeddingProviderException
from app.domain.vector.entities import VectorDocument
from app.domain.vector.repository import VectorRepository


class EmbeddingService:
    """
    Application service responsible for:

    1. Generating embeddings for document chunks.
    2. Creating VectorDocument domain entities.
    3. Persisting vectors through the VectorRepository.
    """

    def __init__(
        self,
        vector_repository: VectorRepository,
        provider: EmbeddingProvider | None = None,
        embedding_model: str = "text-embedding-3-small",
    ):
        self.vector_repository = vector_repository
        self.provider = provider or OpenAIEmbeddingProvider()
        self.embedding_model = embedding_model

    def create_vectors(
        self,
        document_id: int,
        chunks: list[str],
    ) -> list[VectorDocument]:
        """
        Generate embeddings, create VectorDocument entities,
        persist them, and return the stored documents.

        Args:
            document_id: Parent document identifier.
            chunks: Document chunks.

        Returns:
            List of persisted VectorDocument objects.

        Raises:
            EmbeddingProviderException:
                If the embedding provider fails or returns
                an unexpected number of embeddings.
        """

        if not chunks:
            return []

        embeddings = self.provider.generate(chunks)

        if len(embeddings) != len(chunks):
            raise EmbeddingProviderException(
                "Embedding provider returned an unexpected "
                "number of embeddings."
            )

        vector_documents: list[VectorDocument] = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            vector_documents.append(
                VectorDocument(
                    id=uuid4(),
                    document_id=document_id,
                    chunk_index=index,
                    content=chunk,
                    embedding=embedding,
                    embedding_model=self.embedding_model,
                    created_at=datetime.now(UTC),
                )
            )

        # Batch persistence
        self.vector_repository.save_all(vector_documents)

        return vector_documents

    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[VectorDocument]:
        """
        Perform semantic search using a text query.
        """

        query_embedding = self.provider.generate([query])[0]

        return self.vector_repository.similarity_search(
            embedding=query_embedding,
            top_k=top_k,
        )

    def get_vector(
        self,
        vector_id: UUID,
    ) -> VectorDocument | None:
        """
        Retrieve a stored vector document by ID.
        """

        return self.vector_repository.get_by_id(vector_id)

    def delete_vector(
        self,
        vector_id: UUID,
    ) -> None:
        """
        Delete a stored vector document.
        """

        self.vector_repository.delete(vector_id)