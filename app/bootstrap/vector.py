from fastapi import Depends
from sqlalchemy.orm import Session

from app.bootstrap.database import get_db
from app.infrastructure.vector.pgvector_repository import PgVectorRepository


def get_vector_repository(
    db: Session = Depends(get_db),
) -> PgVectorRepository:
    return PgVectorRepository(db)