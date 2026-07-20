from .embedding_provider import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):

    def generate(self, chunks: list[str]) -> list[list[float]]:
        raise NotImplementedError(
            "OpenAI provider not implemented yet."
        )