from uuid import UUID

import pytest

from app.application.ingestion.embedding_service import EmbeddingService
from app.application.ingestion.providers.embedding_provider import EmbeddingProvider
from app.core.exceptions import EmbeddingProviderException


class FakeEmbeddingProvider(EmbeddingProvider):
    """Deterministic provider for unit tests."""

    def __init__(self, embeddings=None, error=None):
        self.embeddings = embeddings
        self.error = error

    def generate(self, chunks: list[str]) -> list[list[float]]:
        if self.error:
            raise self.error

        return self.embeddings or [
            [0.1, 0.2, 0.3]
            for _ in chunks
        ]


class FakeVectorRepository:
    """In-memory repository for unit tests."""

    def __init__(self):
        self.saved_documents = []
        self.deleted_ids = []

    def save_all(self, documents):
        self.saved_documents.extend(documents)

    def similarity_search(self, embedding, top_k=5):
        return self.saved_documents[:top_k]

    def get_by_id(self, vector_id):
        for document in self.saved_documents:
            if document.id == vector_id:
                return document

        return None

    def delete(self, vector_id):
        self.deleted_ids.append(vector_id)


def test_create_vectors_returns_empty_list_for_empty_chunks():
    provider = FakeEmbeddingProvider()
    repository = FakeVectorRepository()

    service = EmbeddingService(
        vector_repository=repository,
        provider=provider,
    )

    result = service.create_vectors(
        document_id=1,
        chunks=[],
    )

    assert result == []
    assert repository.saved_documents == []


def test_create_vectors_creates_one_vector_per_chunk():
    chunks = [
        "first chunk",
        "second chunk",
        "third chunk",
    ]

    embeddings = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
        [0.7, 0.8, 0.9],
    ]

    provider = FakeEmbeddingProvider(
        embeddings=embeddings,
    )

    repository = FakeVectorRepository()

    service = EmbeddingService(
        vector_repository=repository,
        provider=provider,
        embedding_model="test-model",
    )

    result = service.create_vectors(
        document_id=42,
        chunks=chunks,
    )

    assert len(result) == 3
    assert len(repository.saved_documents) == 3

    for index, document in enumerate(result):
        assert isinstance(document.id, UUID)
        assert document.document_id == 42
        assert document.chunk_index == index
        assert document.content == chunks[index]
        assert document.embedding == embeddings[index]
        assert document.embedding_model == "test-model"


def test_create_vectors_rejects_mismatched_embedding_count():
    chunks = [
        "first chunk",
        "second chunk",
        "third chunk",
    ]

    embeddings = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    provider = FakeEmbeddingProvider(
        embeddings=embeddings,
    )

    repository = FakeVectorRepository()

    service = EmbeddingService(
        vector_repository=repository,
        provider=provider,
    )

    with pytest.raises(EmbeddingProviderException):
        service.create_vectors(
            document_id=1,
            chunks=chunks,
        )

    assert repository.saved_documents == []


def test_create_vectors_propagates_embedding_provider_exception():
    provider = FakeEmbeddingProvider(
        error=EmbeddingProviderException(
            "Embedding generation failed."
        )
    )

    repository = FakeVectorRepository()

    service = EmbeddingService(
        vector_repository=repository,
        provider=provider,
    )

    with pytest.raises(EmbeddingProviderException):
        service.create_vectors(
            document_id=1,
            chunks=["test chunk"],
        )

    assert repository.saved_documents == []


def test_get_vector_returns_matching_vector():
    provider = FakeEmbeddingProvider()
    repository = FakeVectorRepository()

    service = EmbeddingService(
        vector_repository=repository,
        provider=provider,
    )

    result = service.create_vectors(
        document_id=10,
        chunks=["test chunk"],
    )

    vector_id = result[0].id

    retrieved = service.get_vector(vector_id)

    assert retrieved is not None
    assert retrieved.id == vector_id
    assert retrieved.content == "test chunk"


def test_delete_vector_delegates_to_repository():
    provider = FakeEmbeddingProvider()
    repository = FakeVectorRepository()

    service = EmbeddingService(
        vector_repository=repository,
        provider=provider,
    )

    result = service.create_vectors(
        document_id=10,
        chunks=["test chunk"],
    )

    vector_id = result[0].id

    service.delete_vector(vector_id)

    assert repository.deleted_ids == [vector_id]