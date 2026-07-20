from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from environment variables
    and optionally from a local .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ----------------------------------------
    # Application
    # ----------------------------------------

    APP_NAME: str = "Patel Data Ingestion Pipeline"

    DEBUG: bool = True

    # ----------------------------------------
    # Storage
    # ----------------------------------------

    UPLOAD_DIRECTORY: str = "uploads"

    # ----------------------------------------
    # Database
    # ----------------------------------------

    DATABASE_URL: str = "sqlite:///./ingestion.db"

    # ----------------------------------------
    # OpenAI
    # ----------------------------------------

    OPENAI_API_KEY: str = ""

    EMBEDDING_MODEL: str = "text-embedding-3-small"


settings = Settings()