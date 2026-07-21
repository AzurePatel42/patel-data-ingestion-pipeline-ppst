from app.application.ingestion.providers.openai_provider import OpenAIEmbeddingProvider
from app.application.ingestion.embedding_service import EmbeddingService


def main():
    provider = OpenAIEmbeddingProvider()
    service = EmbeddingService(provider)

    chunks = [
        "Patel Engineering builds production-ready backend systems.",
        "PPST provides a reusable backend platform.",
    ]

    vectors = service.generate_embeddings(chunks)

    print(f"Generated {len(vectors)} embeddings")
    print(f"Embedding dimension: {len(vectors[0])}")
    print(f"First 5 values: {vectors[0][:5]}")


if __name__ == "__main__":
    main()