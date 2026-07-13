from sqlalchemy import Column, Integer, String

from app.infrastructure.db.session import Base


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    file_type = Column(String)

    status = Column(String)

    created_at = Column(String)