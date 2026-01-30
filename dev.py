import uvicorn
import asyncio
from backend.app.db.base import Base
from backend.app.db.session import engine

async def init_db():
    # Only for local dev with SQLite
    # In production/docker, use Alembic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Local Database initialized (SQLite).")

if __name__ == "__main__":
    # Check if we should init db (e.g., if sqlite is used)
    from backend.app.core.config import settings
    if settings.async_database_url.startswith("sqlite"):
        asyncio.run(init_db())
    
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8001, reload=True)
