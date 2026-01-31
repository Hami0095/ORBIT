import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from backend.app.main import app
from backend.app.db.base import Base
from backend.app.db.session import get_db
from backend.app.core.config import settings

# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture
async def test_db(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(test_db) -> AsyncGenerator[AsyncClient, None]:
    """Create a test HTTP client with database dependency override."""
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
def mock_watsonx(mocker):
    """Mock all watsonx service calls to avoid external dependencies."""
    return mocker.patch(
        "backend.app.services.watsonx_service.WatsonxService.run_agent",
        return_value={
            "status": "success",
            "agent_id": "mock_agent",
            "correlation_id": "wx-9999",
            "response_metadata": {"model": "granite-20b-instruct", "token_count": 250},
            "tasks": [
                {"title": "Mock Task 1", "description": "First mock task from watsonx"},
                {"title": "Mock Task 2", "description": "Second mock task from watsonx"},
                {"title": "Mock Task 3", "description": "Third mock task from watsonx"}
            ]
        }
    )
