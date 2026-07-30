from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine


def initialize_database() -> None:
    """
    Initialize the application database.

    During development this creates missing tables.
    In production this can be replaced by Alembic migrations.
    """

    Base.metadata.create_all(bind=engine)