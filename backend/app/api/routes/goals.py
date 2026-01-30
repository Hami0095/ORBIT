from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.repositories.goal_repository import goal_repo
from backend.app.schemas.goal import Goal, GoalCreate
from backend.app.db.models import User

router = APIRouter()

@router.post("/", response_model=Goal)
async def create_goal(
    *,
    db: AsyncSession = Depends(deps.get_db),
    goal_in: GoalCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    return await goal_repo.create_with_owner(db, obj_in=goal_in, owner_id=current_user.id)

@router.get("/", response_model=List[Goal])
async def read_goals(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    return await goal_repo.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)

@router.get("/{id}", response_model=Goal)
async def read_goal(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    goal = await goal_repo.get(db, id=id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal.created_by != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return goal
