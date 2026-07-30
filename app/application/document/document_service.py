import logging
from uuid import UUID

from app.application.contracts.document_schemas import DocumentResponse
from app.core.exceptions import NotFoundException
from app.domain.document.document_status import DocumentStatus
from app.events.event_bus import EventBus

logger = logging.getLogger(__name__)


class DocumentService:

    def __init__(self, repo):
        self.repo = repo

    def create_document(self, filename: str) -> DocumentResponse:
        """
        Create a new document record.
        """

        file_type = (
            filename.rsplit(".", 1)[1].lower()
            if "." in filename
            else "unknown"
        )

        document = self.repo.create(
            filename=filename,
            file_type=file_type,
            status=DocumentStatus.UPLOADED.value,
        )

        logger.info(
            "Created document %s (%s)",
            document.id,
            filename,
        )

        EventBus.publish(
            "document_uploaded",
            {
                "document_id": document.id,
            },
        )

        return self._to_response(document)

    def get_documents(self) -> list[DocumentResponse]:
        """
        Retrieve all documents.
        """

        documents = self.repo.get_all()

        logger.info(
            "Retrieved %d documents",
            len(documents),
        )

        return [
            self._to_response(document)
            for document in documents
        ]

    def get_document(
        self,
        document_id: UUID,
    ) -> DocumentResponse:
        """
        Retrieve a document by ID.
        """

        document = self.repo.get_by_id(document_id)

        if document is None:
            raise NotFoundException(
                "Document not found."
            )

        logger.info(
            "Retrieved document %s",
            document_id,
        )

        return self._to_response(document)

    def update_document(
        self,
        document_id: UUID,
        data: dict,
    ) -> DocumentResponse:
        """
        Update a document.
        """

        document = self.repo.get_by_id(document_id)

        if document is None:
            raise NotFoundException(
                "Document not found."
            )

        updated_document = self.repo.update(
            document,
            data,
        )

        logger.info(
            "Updated document %s",
            document_id,
        )

        return self._to_response(updated_document)

    def delete_document(
        self,
        document_id: UUID,
    ) -> None:
        """
        Delete a document.
        """

        document = self.repo.get_by_id(document_id)

        if document is None:
            raise NotFoundException(
                "Document not found."
            )

        self.repo.delete(document)

        logger.info(
            "Deleted document %s",
            document_id,
        )

    def update_document_status(
        self,
        document_id: UUID,
        status: DocumentStatus,
    ) -> DocumentResponse:
        """
        Update the document processing status.
        """

        document = self.repo.get_by_id(document_id)

        if document is None:
            raise NotFoundException(
                "Document not found."
            )

        updated_document = self.repo.update(
            document,
            {
                "status": status.value,
            },
        )

        logger.info(
            "Updated document %s status to %s",
            document_id,
            status.value,
        )

        return self._to_response(updated_document)

    def _to_response(
        self,
        document,
    ) -> DocumentResponse:
        return DocumentResponse(
            id=document.id,
            filename=document.filename,
            status=document.status,
        )