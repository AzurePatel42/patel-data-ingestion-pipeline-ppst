from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):

    @abstractmethod
    def generate(self, chunks: list[str]) -> list[list[float]]:
        """
        Generate embeddings for text chunks.
        """
        pass