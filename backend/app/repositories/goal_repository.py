from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.repositories.base import BaseRepository
from backend.app.db.models import Goal
from backend.app.schemas.goal import GoalCreate, GoalUpdate

class GoalRepository(BaseRepository[Goal, GoalCreate, GoalUpdate]):
    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: GoalCreate, owner_id: int
    ) -> Goal:
        db_obj = Goal(
            **obj_in.model_dump(),
            created_by=owner_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Goal]:
        result = await db.execute(
            select(Goal)
            .filter(Goal.created_by == owner_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

goal_repo = GoalRepository(Goal)
