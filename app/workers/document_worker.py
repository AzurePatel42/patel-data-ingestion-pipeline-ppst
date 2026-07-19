from app.application.ingestion.text_extractor import TextExtractor
from app.domain.document.document_status import DocumentStatus


class DocumentWorker:

    @staticmethod
    def process(document):

        print(f"Processing document {document.id}")

        document.status = DocumentStatus.PROCESSING

        # Step 1
        
        text = TextExtractor.extract(document.file_path)

        print(text)

        document.status = DocumentStatus.COMPLETED

        