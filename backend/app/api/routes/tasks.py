from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.repositories.task_repository import task_repo
from backend.app.schemas.task import Task, TaskUpdate
from backend.app.db.models import User

router = APIRouter()

@router.get("/", response_model=List[Task])
async def read_tasks(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    # In a real app, we might filter tasks by goals owned by the user
    return await task_repo.get_multi(db, skip=skip, limit=limit)

@router.patch("/{id}", response_model=Task)
async def update_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    task_in: TaskUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    task = await task_repo.get(db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await task_repo.update(db, db_obj=task, obj_in=task_in)
