import asyncio
import sys
from pathlib import Path

# Add the project root to sys.path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from backend.app.db.session import engine
from backend.app.db.base import Base
from backend.app.db.models import User, TeamMember, Goal, Task, Schedule, AgentLog, Integration # Import models to ensure they are registered

async def init_db():
    async with engine.begin() as conn:
        print("Creating tables...")
        # In a real app with migrations, you'd use alembic
        # For this setup, we'll use create_all
        await conn.run_sync(Base.metadata.create_all)
        print("Database initialized successfully!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
