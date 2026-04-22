from fastapi import FastAPI
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
app = FastAPI(title="Internship Partnership Platform")

@app.get("/health")
async def health():
    db_status = "not checked"
    redis_status = "not checked"

    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text
        engine = create_async_engine(settings.database_url)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    try:
        from redis.asyncio import Redis
        r = Redis.from_url(settings.redis_url)
        await r.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"error: {str(e)}"

    return {"status": "ok", "db": db_status, "redis": redis_status}