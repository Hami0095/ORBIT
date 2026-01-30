from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.repositories.base import BaseRepository
from backend.app.db.models import Task
from backend.app.schemas.task import TaskCreate, TaskUpdate

class TaskRepository(BaseRepository[Task, TaskCreate, TaskUpdate]):
    async def get_multi_by_goal(
        self, db: AsyncSession, *, goal_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        result = await db.execute(
            select(Task)
            .filter(Task.goal_id == goal_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

task_repo = TaskRepository(Task)
