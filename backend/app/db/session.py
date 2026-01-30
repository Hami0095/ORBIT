from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.app.core.config import settings

engine = create_async_engine(
    settings.async_database_url,
    echo=True,
    future=True,
    connect_args={"check_same_thread": False} if settings.async_database_url.startswith("sqlite") else {}
)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with SessionLocal() as session:
        yield session
        await session.commit()
