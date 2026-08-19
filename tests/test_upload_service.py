from io import BytesIO

from fastapi import UploadFile

from app.application.ingestion.upload_service import UploadService
from app.core.exceptions import EmptyDocumentException
from app.domain.document.document_status import DocumentStatus


class FakeDocument:
    """Simple document representation for upload tests."""

    def __init__(
        self,
        document_id: int,
        filename: str,
        status: str,
    ):
        self.id = document_id
        self.filename = filename
        self.status = status


class FakeDocumentService:
    """Fake document service for upload-service tests."""

    def __init__(self):
        self.created_documents = []
        self.status_updates = []

    def create_document(self, filename: str):
        document = FakeDocument(
            document_id=10,
            filename=filename,
            status=DocumentStatus.UPLOADED.value,
        )

        self.created_documents.append(document)

        return document

    def update_document_status(
        self,
        document_id: int,
        status: DocumentStatus,
    ):
        self.status_updates.append(
            {
                "document_id": document_id,
                "status": status,
            }
        )

        document = self.created_documents[0]
        document.status = status.value

        return document


class FakeIngestionService:
    """Fake ingestion service for upload-service tests."""

    def __init__(self):
        self.document_id = None
        self.file_path = None

    def ingest_document(
        self,
        document_id: int,
        file_path,
    ):
        self.document_id = document_id
        self.file_path = file_path

        return [
            {
                "document_id": document_id,
                "content": "test content",
            }
        ]


def create_upload_file(
    filename: str,
    content: bytes,
) -> UploadFile:
    return UploadFile(
        filename=filename,
        file=BytesIO(content),
    )


def test_upload_marks_document_completed():
    document_service = FakeDocumentService()
    ingestion_service = FakeIngestionService()

    service = UploadService(
        document_service=document_service,
        ingestion_service=ingestion_service,
    )

    file = create_upload_file(
        filename="test.txt",
        content=b"test content",
    )

    result = service.upload(file)

    assert result.document_id == 10
    assert result.filename == "test.txt"
    assert result.status == DocumentStatus.COMPLETED
    assert result.vectors_created == 1

    assert document_service.status_updates == [
        {
            "document_id": 10,
            "status": DocumentStatus.COMPLETED,
        }
    ]

    assert ingestion_service.document_id == 10
    assert ingestion_service.file_path is not None


def test_upload_rejects_empty_file():
    document_service = FakeDocumentService()
    ingestion_service = FakeIngestionService()

    service = UploadService(
        document_service=document_service,
        ingestion_service=ingestion_service,
    )

    file = create_upload_file(
        filename="empty.txt",
        content=b"",
    )

    try:
        service.upload(file)
        assert False, "Expected EmptyDocumentException"
    except EmptyDocumentException:
        pass

    assert document_service.created_documents == []
    assert document_service.status_updates == []
    assert ingestion_service.document_id is None