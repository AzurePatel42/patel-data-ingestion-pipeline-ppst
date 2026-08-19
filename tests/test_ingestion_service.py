from pathlib import Path

import pytest

from app.application.ingestion.ingestion_service import IngestionService
from app.core.exceptions import EmptyDocumentException
from app.core.exceptions import UnsupportedDocumentException


class FakeChunkingService:
    """Deterministic chunking service for unit tests."""

    def __init__(self):
        self.received_text = None

    def chunk(self, text: str) -> list[str]:
        self.received_text = text
        return [text]


class FakeEmbeddingService:
    """Deterministic embedding service for unit tests."""

    def __init__(self):
        self.document_id = None
        self.chunks = None

    def create_vectors(self, document_id: int, chunks: list[str]):
        self.document_id = document_id
        self.chunks = chunks

        return [
            {
                "document_id": document_id,
                "content": chunk,
            }
            for chunk in chunks
        ]


def test_ingest_text_rejects_empty_text():
    embedding_service = FakeEmbeddingService()

    service = IngestionService(
        embedding_service=embedding_service,
    )

    with pytest.raises(EmptyDocumentException):
        service.ingest_text(
            document_id=1,
            text="",
        )


def test_ingest_text_rejects_whitespace_only_text():
    embedding_service = FakeEmbeddingService()

    service = IngestionService(
        embedding_service=embedding_service,
    )

    with pytest.raises(EmptyDocumentException):
        service.ingest_text(
            document_id=1,
            text="   \n\t  ",
        )


def test_ingest_text_passes_text_to_chunking_and_embedding():
    embedding_service = FakeEmbeddingService()
    chunking_service = FakeChunkingService()

    service = IngestionService(
        embedding_service=embedding_service,
        chunking_service=chunking_service,
    )

    result = service.ingest_text(
        document_id=42,
        text="This is test document content.",
    )

    assert chunking_service.received_text == (
        "This is test document content."
    )

    assert embedding_service.document_id == 42
    assert embedding_service.chunks == [
        "This is test document content."
    ]

    assert result == [
        {
            "document_id": 42,
            "content": "This is test document content.",
        }
    ]


def test_ingest_document_extracts_and_ingests_text(tmp_path):
    file_path = tmp_path / "sample.txt"

    file_path.write_text(
        "This is a test document.",
        encoding="utf-8",
    )

    embedding_service = FakeEmbeddingService()
    chunking_service = FakeChunkingService()

    service = IngestionService(
        embedding_service=embedding_service,
        chunking_service=chunking_service,
    )

    result = service.ingest_document(
        document_id=100,
        file_path=file_path,
    )

    assert embedding_service.document_id == 100
    assert embedding_service.chunks == [
        "This is a test document."
    ]

    assert result == [
        {
            "document_id": 100,
            "content": "This is a test document.",
        }
    ]


def test_ingest_document_rejects_unsupported_file_type(tmp_path):
    file_path = tmp_path / "sample.exe"

    file_path.write_text(
        "not a supported document",
        encoding="utf-8",
    )

    embedding_service = FakeEmbeddingService()

    service = IngestionService(
        embedding_service=embedding_service,
    )

    with pytest.raises(UnsupportedDocumentException):
        service.ingest_document(
            document_id=1,
            file_path=file_path,
        )