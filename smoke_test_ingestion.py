from uuid import uuid4

from app.application.ingestion.embedding_service import EmbeddingService
from app.application.ingestion.ingestion_service import IngestionService
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.vector.pgvector_repository import PgVectorRepository


def main():
    db = SessionLocal()

    try:
        # Repository
        vector_repository = PgVectorRepository(db)

        # Services
        embedding_service = EmbeddingService(vector_repository)
        ingestion_service = IngestionService(embedding_service)

        # Sample document
        document_id = uuid4()

        sample_text = """
Azure Blob Storage is Microsoft's object storage solution.

Azure Files provides fully managed file shares.

Azure Queue Storage enables reliable asynchronous messaging.

Azure Table Storage stores large amounts of structured NoSQL data.
"""

        print("=" * 60)
        print("Starting ingestion...")
        print("=" * 60)

        # Ingest
        vector_documents = ingestion_service.ingest_text(
            document_id=document_id,
            text=sample_text,
        )

        print(f"\n✓ Stored {len(vector_documents)} vector documents")

        # Verify one document exists
        first_vector = vector_repository.get_by_id(vector_documents[0].id)

        if first_vector is None:
            raise RuntimeError("Failed to retrieve stored vector.")

        print("\n✓ Successfully retrieved vector by ID")
        print(f"Chunk Index : {first_vector.chunk_index}")
        print(f"Model       : {first_vector.embedding_model}")

        print("\nContent Preview:")
        print(first_vector.content[:100])

        # Similarity Search
        print("\nRunning similarity search...")

        results = embedding_service.similarity_search(
            query="What is Azure Blob Storage?",
            top_k=3,
        )

        print(f"\nReturned {len(results)} similar documents\n")

        for i, doc in enumerate(results, start=1):
            print(f"Result {i}")
            print("-" * 50)
            print(doc.content[:200])
            print()

        print("=" * 60)
        print("✓ INGESTION PIPELINE SMOKE TEST PASSED")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()