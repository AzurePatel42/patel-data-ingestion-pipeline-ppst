from app.infrastructure.db.session import Base, engine

# Import ALL models here so SQLAlchemy registers them
from app.infrastructure.vector.models import VectorDocumentModel


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()