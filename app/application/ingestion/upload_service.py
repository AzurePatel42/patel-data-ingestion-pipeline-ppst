from pathlib import Path
import logging
import tempfile

from fastapi import UploadFile

from app.application.contracts.upload_schemas import UploadResponse
from app.application.document.document_service import DocumentService
from app.application.ingestion.ingestion_service import IngestionService
from app.core.exceptions import (
    AppException,
    EmptyDocumentException,
    ValidationException,
)
from app.domain.document.document_status import DocumentStatus

logger = logging.getLogger(__name__)


class UploadService:

    def __init__(
        self,
        document_service: DocumentService,
        ingestion_service: IngestionService,
    ):
        self.document_service = document_service
        self.ingestion_service = ingestion_service

    def upload(self, file: UploadFile) -> UploadResponse:
        """
        Upload a document, ingest its contents,
        generate embeddings, and persist vectors.
        """

        temp_path: Path | None = None

        try:

            logger.info(
                "Starting upload for '%s'",
                file.filename,
            )

            if not file.filename:
                raise ValidationException(
                    "Filename is required."
                )

            file_contents = file.file.read()

            if not file_contents:
                raise EmptyDocumentException(
                    "Uploaded file is empty."
                )

            document = self.document_service.create_document(
                filename=file.filename,
            )

            logger.info(
                "Created document metadata (id=%s)",
                document.id,
            )

            suffix = Path(file.filename).suffix

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            ) as temp:

                temp.write(file_contents)
                temp_path = Path(temp.name)

            logger.debug(
                "Temporary file created: %s",
                temp_path,
            )

            vectors = self.ingestion_service.ingest_document(
                document_id=document.id,
                file_path=temp_path,
            )

            logger.info(
                "Generated %d vectors for document %s",
                len(vectors),
                document.id,
            )

            response = UploadResponse(
                document_id=document.id,
                filename=document.filename,
                status=DocumentStatus.COMPLETED,
                vectors_created=len(vectors),
            )

            logger.info(
                "Upload completed successfully for document %s",
                document.id,
            )

            return response

        except AppException:

            logger.exception(
                "Application error while uploading '%s'",
                file.filename,
            )

            raise

        except Exception as ex:

            logger.exception(
                "Unexpected error while uploading '%s'",
                file.filename,
            )

            raise AppException(
                "Unexpected error occurred while uploading document."
            ) from ex

        finally:

            if temp_path and temp_path.exists():

                logger.debug(
                    "Removing temporary file %s",
                    temp_path,
                )

                temp_path.unlink()

                logger.debug(
                    "Temporary file removed successfully."
                )