from fastapi import FastAPI
from app.config import settings
from app.db import engine, Base

app = FastAPI(title="Internship Partnership Platform")

@app.on_event("startup")
async def startup():
    
    from app.models import user
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health():
    db_status = "not checked"
    redis_status = "not checked"

    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text
        test_engine = create_async_engine(settings.database_url)
        async with test_engine.connect() as conn:
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