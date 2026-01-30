from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.orchestrator.orbit_orchestrator import orbit_orchestrator
from backend.app.repositories.goal_repository import goal_repo
from backend.app.schemas.goal import GoalCreate
from backend.app.db.models import User
from pydantic import BaseModel

class OrchestrationRequest(BaseModel):
    goal_text: str

router = APIRouter()

@router.post("/start")
async def start_orchestration(
    *,
    db: AsyncSession = Depends(deps.get_db),
    request: OrchestrationRequest,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    # 1. Save goal
    goal_in = GoalCreate(
        title=request.goal_text[:50] + "...",
        description=request.goal_text
    )
    goal = await goal_repo.create_with_owner(db, obj_in=goal_in, owner_id=current_user.id)
    
    # 2. Call orchestrator
    result = await orbit_orchestrator.orchestrate(db, goal_id=goal.id, goal_text=request.goal_text)
    
    return {
        "goal_id": goal.id,
        "orchestration_result": result
    }
