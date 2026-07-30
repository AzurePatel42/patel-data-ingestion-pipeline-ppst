from pathlib import Path
from uuid import UUID

from app.application.extraction.extractor_factory import ExtractorFactory
from app.application.ingestion.chunking_service import ChunkingService
from app.application.ingestion.embedding_service import EmbeddingService
from app.domain.vector.entities import VectorDocument


class IngestionService:
    """
    Orchestrates the complete document ingestion pipeline.

    Pipeline:
        File
          ↓
    ExtractorFactory
          ↓
    Document Extractor
          ↓
    Chunking
          ↓
    Embedding Generation
          ↓
    Vector Persistence
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        chunking_service: ChunkingService | None = None,
    ):
        self.embedding_service = embedding_service
        self.chunking_service = chunking_service or ChunkingService()

    def ingest_text(
        self,
        document_id: UUID,
        text: str,
    ) -> list[VectorDocument]:
        """
        Ingest raw text into the vector database.
        """

        chunks = self.chunking_service.chunk(text)

        return self.embedding_service.create_vectors(
            document_id=document_id,
            chunks=chunks,
        )

    def ingest_document(
        self,
        document_id: UUID,
        file_path: Path,
    ) -> list[VectorDocument]:
        """
        Extract text from a document and ingest it.
        """

        extractor = ExtractorFactory.get_extractor(
            file_path.suffix
        )

        text = extractor.extract(file_path)

        return self.ingest_text(
            document_id=document_id,
            text=text,
        )