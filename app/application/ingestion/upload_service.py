from pathlib import Path
import tempfile

from fastapi import UploadFile

from app.application.contracts.upload_schemas import UploadResponse
from app.application.document.document_service import DocumentService
from app.application.ingestion.ingestion_service import IngestionService
from app.domain.document.document_status import DocumentStatus


class UploadService:

    def __init__(
        self,
        document_service: DocumentService,
        ingestion_service: IngestionService,
    ):
        self.document_service = document_service
        self.ingestion_service = ingestion_service

    def upload(self, file: UploadFile):

        temp_path = None

        try:

            # Create document metadata
            document = self.document_service.create_document(
                filename=file.filename,
            )

            suffix = Path(file.filename).suffix

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            ) as temp:

                temp.write(file.file.read())
                temp_path = Path(temp.name)

            vectors = self.ingestion_service.ingest_file(
                document_id=document.id,
                file_path=temp_path,
            )

            return UploadResponse(
                document_id=document.id,
                filename=document.filename,
                status=DocumentStatus.COMPLETED,
                vectors_created=len(vectors),
            )

        finally:

            if temp_path and temp_path.exists():
                temp_path.unlink()