from openai import OpenAI

from app.core.config import settings
from app.application.ingestion.providers.embedding_provider import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, chunks: list[str]) -> list[list[float]]:

        response = self.client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=chunks,
        )

        return [item.embedding for item in response.data]