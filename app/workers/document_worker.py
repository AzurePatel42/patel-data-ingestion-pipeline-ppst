from app.domain.document.document_status import DocumentStatus


class DocumentWorker:

    @staticmethod
    def process(document):

        print(f"Processing document {document.id}")

        document.status = DocumentStatus.PROCESSING

        # Step 1
        print("Extracting text...")

        # Step 2
        print("Chunking document...")

        # Step 3
        print("Generating embeddings...")

        document.status = DocumentStatus.COMPLETED

        print(f"Document {document.id} completed")