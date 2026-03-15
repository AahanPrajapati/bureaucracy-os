"""Application configuration settings."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Bureaucracy OS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    POSTGRES_URL: str = "postgresql://postgres:postgres@localhost:5432/bureaucracy_os"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "workflow-events"

    # AI / LLM
    ANTHROPIC_API_KEY: str = ""
    AI_MODEL: str = "claude-sonnet-4-20250514"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"


settings = Settings()
