from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "ORBIT - AI Task Orchestrator"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "development-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "orbit"
    
    # If DATABASE_URL is not provided, we will default to SQLite for easy local dev
    # or build the Postgres URL for Docker.
    DATABASE_URL: Optional[str] = None

    @property
    def async_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        # Default to SQLite for local development to avoid manual Postgres installation
        # Change this to use Postgres by setting DATABASE_URL in .env
        return "sqlite+aiosqlite:///./orbit.db"

    # IBM watsonx
    WATSONX_API_KEY: Optional[str] = None
    WATSONX_PROJECT_ID: Optional[str] = None
    WATSONX_URL: str = "https://us-south.ml.cloud.ibm.com"

    # Dev/Prod toggle
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
