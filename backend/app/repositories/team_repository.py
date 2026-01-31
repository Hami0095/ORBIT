from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.base import BaseRepository
from backend.app.db.models import TeamMember
from backend.app.schemas.team import TeamMemberCreate, TeamMemberUpdate

class TeamRepository(BaseRepository[TeamMember, TeamMemberCreate, TeamMemberUpdate]):
    async def create_with_manager(
        self, db: AsyncSession, *, obj_in: TeamMemberCreate, manager_id: int
    ) -> TeamMember:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, manager_id=manager_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_manager(
        self, db: AsyncSession, *, manager_id: int, skip: int = 0, limit: int = 100
    ) -> list[TeamMember]:
        from sqlalchemy.future import select
        result = await db.execute(
            select(self.model)
            .filter(self.model.manager_id == manager_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

team_repo = TeamRepository(TeamMember)
