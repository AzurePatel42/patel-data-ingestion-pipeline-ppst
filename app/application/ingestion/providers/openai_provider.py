from openai import OpenAI

from app.application.ingestion.providers.embedding_provider import EmbeddingProvider
from app.core.config import settings
from app.core.exceptions import EmbeddingProviderException


class OpenAIEmbeddingProvider(EmbeddingProvider):

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, chunks: list[str]) -> list[list[float]]:
        try:
            response = self.client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=chunks,
            )

            return [item.embedding for item in response.data]

        except Exception as exc:
            raise EmbeddingProviderException(
                "Failed to generate embeddings."
            ) from exc