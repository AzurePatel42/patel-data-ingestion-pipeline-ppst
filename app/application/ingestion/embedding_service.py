from app.application.ingestion.providers.embedding_provider import EmbeddingProvider


class EmbeddingService:
    """
    Application service responsible for generating embeddings
    for document chunks.
    """

    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    def generate_embeddings(self, chunks: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of text chunks.

        Args:
            chunks: List of text chunks.

        Returns:
            List of embedding vectors.
        """
        return self.provider.generate(chunks)