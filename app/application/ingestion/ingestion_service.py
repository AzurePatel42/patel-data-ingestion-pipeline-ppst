from uuid import UUID

from app.application.ingestion.chunking_service import ChunkingService
from app.application.ingestion.embedding_service import EmbeddingService
from app.application.ingestion.text_extractor import TextExtractor
from app.domain.vector.entities import VectorDocument


class IngestionService:
    """
    Orchestrates the complete document ingestion pipeline.

    Pipeline:
        File/Text
            ↓
        Text Extraction
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
        text_extractor: TextExtractor | None = None,
    ):
        self.embedding_service = embedding_service
        self.chunking_service = chunking_service or ChunkingService()
        self.text_extractor = text_extractor or TextExtractor()

    def ingest_text(
        self,
        document_id: UUID,
        text: str,
    ) -> list[VectorDocument]:
        """
        Ingest raw text into the vector database.

        Args:
            document_id: Parent document ID.
            text: Raw text content.

        Returns:
            Persisted VectorDocument objects.
        """

        chunks = self.chunking_service.chunk(text)

        return self.embedding_service.ingest(
            document_id=document_id,
            chunks=chunks,
        )

    def ingest_file(
        self,
        document_id: UUID,
        file_path: str,
    ) -> list[VectorDocument]:
        """
        Extract text from a file and ingest it.

        Args:
            document_id: Parent document ID.
            file_path: Path to the document.

        Returns:
            Persisted VectorDocument objects.
        """

        text = self.text_extractor.extract(file_path)

        return self.ingest_text(
            document_id=document_id,
            text=text,
        )