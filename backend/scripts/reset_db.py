import asyncio
import sys
import os
from pathlib import Path

# Add the project root (ORBIT) to sys.path
# __file__ is ORBIT/backend/scripts/reset_db.py
# .parent is ORBIT/backend/scripts
# .parent.parent is ORBIT/backend
# .parent.parent.parent is ORBIT
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

from backend.app.db.session import engine
from backend.app.db.base import Base
from backend.app.db.models import User, TeamMember, Goal, Task, Schedule, AgentLog, Integration

async def reset_db():
    async with engine.begin() as conn:
        print("🔥 Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("🚀 Creating all tables with new schema...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database reset successfully!")
    await engine.dispose()

if __name__ == "__main__":
    force = "--force" in sys.argv
    
    if force:
        asyncio.run(reset_db())
    else:
        confirm = input("This will DELETE ALL DATA. Are you sure? (y/N): ")
        if confirm.lower() == 'y':
            asyncio.run(reset_db())
        else:
            print("Operation cancelled. Use --force to skip this prompt.")
