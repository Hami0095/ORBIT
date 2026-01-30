from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models import AgentLog

class AgentLogRepository:
    async def create(self, db: AsyncSession, *, agent_name: str, action: str, payload: dict) -> AgentLog:
        db_obj = AgentLog(
            agent_name=agent_name,
            action=action,
            payload_json=payload
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

agent_log_repo = AgentLogRepository()
