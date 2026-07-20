from .providers.embedding_provider import EmbeddingProvider


class EmbeddingService:

    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    def generate(self, chunks: list[str]) -> list[list[float]]:
        """
        Generate embeddings using the configured provider.
        """

        return self.provider.generate(chunks)