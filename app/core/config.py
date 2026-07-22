from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Patel Data Ingestion Pipeline"
    DEBUG: bool = True

    UPLOAD_DIRECTORY: str = "uploads"

    DATABASE_URL: str = "sqlite:///./ingestion.db"

    OPENAI_API_KEY: str 


    EMBEDDING_MODEL: str = "text-embedding-3-small"


settings = Settings()