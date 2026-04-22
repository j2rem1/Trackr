from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/internship"
    redis_url: str = "redis://localhost:6379"
    minio_url: str = "http://localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    secret_key: str = "changethis123"

    class Config:
        env_file = ".env"

settings = Settings()