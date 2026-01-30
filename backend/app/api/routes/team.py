from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.repositories.team_repository import team_repo
from backend.app.schemas.team import TeamMember, TeamMemberCreate
from backend.app.db.models import User

router = APIRouter()

@router.post("/", response_model=TeamMember)
async def create_team_member(
    *,
    db: AsyncSession = Depends(deps.get_db),
    team_in: TeamMemberCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    return await team_repo.create(db, obj_in=team_in)

@router.get("/", response_model=List[TeamMember])
async def read_team(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    return await team_repo.get_multi(db, skip=skip, limit=limit)
