from app.infrastructure.db.models import DocumentModel


class DocumentRepository:

    def __init__(self, db):
        self.db = db

    def create(self, filename: str, file_type: str, status: str):
        document = DocumentModel(filename=filename, file_type=file_type, status=status)

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document

    def get_all(self):
        return self.db.query(DocumentModel).all()

    def get_by_id(self, document_id: int):
        return self.db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    
    def update(self, document: DocumentModel, data: dict):
        for key, value in data.items():
            setattr(document, key, value)

        self.db.commit()
        self.db.refresh(document)
        return document

    def delete(self, document: DocumentModel):
        self.db.delete(document)
        self.db.commit()