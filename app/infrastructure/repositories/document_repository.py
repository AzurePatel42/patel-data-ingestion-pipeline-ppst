import logging

from app.infrastructure.db.models import DocumentModel

logger = logging.getLogger(__name__)


class DocumentRepository:

    def __init__(self, db):
        self.db = db

    def create(
        self,
        filename: str,
        file_type: str,
        status: str,
    ) -> DocumentModel:
        """
        Create a new document.
        """

        document = DocumentModel(
            filename=filename,
            file_type=file_type,
            status=status,
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        logger.info(
            "Document created: %s",
            document.id,
        )

        return document

    def get_all(self) -> list[DocumentModel]:
        """
        Retrieve all documents.
        """

        return (
            self.db.query(DocumentModel)
            .all()
        )

    def get_by_id(
        self,
        document_id: int,
    ) -> DocumentModel | None:
        """
        Retrieve a document by ID.
        """

        return (
            self.db.query(DocumentModel)
            .filter(DocumentModel.id == document_id)
            .first()
        )

    def update(
        self,
        document: DocumentModel,
        data: dict,
    ) -> DocumentModel:
        """
        Update a document.
        """

        for key, value in data.items():
            setattr(document, key, value)

        self.db.commit()
        self.db.refresh(document)

        logger.info(
            "Document updated: %s",
            document.id,
        )

        return document

    def delete(
        self,
        document: DocumentModel,
    ) -> None:
        """
        Delete a document.
        """

        self.db.delete(document)
        self.db.commit()

        logger.info(
            "Document deleted: %s",
            document.id,
        )