from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):

    @abstractmethod
    def generate(self, chunks: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of text chunks."""
        pass