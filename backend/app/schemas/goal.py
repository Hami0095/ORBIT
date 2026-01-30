from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from backend.app.db.models import GoalStatus

class GoalBase(BaseModel):
    title: str
    description: str

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[GoalStatus] = None

class GoalInDBBase(GoalBase):
    id: int
    status: GoalStatus
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class Goal(GoalInDBBase):
    pass

class GoalWithTasks(Goal):
    tasks: List[dict] # Will be Task schema
