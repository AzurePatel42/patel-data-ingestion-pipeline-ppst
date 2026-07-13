from app.domain.document.document_rules import DocumentRules
from app.application.contracts.document_schemas import DocumentResponse
from app.core.exceptions import NotFoundException


class DocumentService:

    def __init__(self, repo):
        self.repo = repo

    def create_document(self, filename: str):

        document = self.repo.create(filename=filename)

        return self._to_response(document)

    def get_documents(self):

        documents = self.repo.get_all()

        return [
            self._to_response(document)
            for document in documents
        ]

    def get_document(self, document_id: int):

        document = self.repo.get_by_id(document_id)

        if document is None:
            raise NotFoundException("Document not found")

        return self._to_response(document)

    def update_document(self, document_id: int, filename: str | None):

        document = self.repo.update(
            document_id,
            filename=filename
        )

        if document is None:
            raise NotFoundException("Document not found")

        return self._to_response(document)

    def delete_document(self, document_id: int):

        deleted = self.repo.get_by_id(document_id)
        if not deleted:
            raise NotFoundException("Document not found")

        self.repo.delete(deleted)
        return {"message": "Document deleted successfully"}

    def _to_response(self, document):

        return DocumentResponse(
            id=document.id,
            filename=document.filename,
            supported=DocumentRules.is_supported_file(
                document.filename
            )
        )
    