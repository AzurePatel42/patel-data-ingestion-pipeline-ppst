from pydantic import BaseModel
import os


class Settings(BaseModel):
    APP_NAME: str = "Patel Data Ingestion Pipeline"
    DEBUG: bool = True

    UPLOAD_DIRECTORY: str = "uploads"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./ingestion.db"
    )


settings = Settings()