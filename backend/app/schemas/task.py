from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from backend.app.db.models import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: str
    priority_score: float = 0.0
    status: TaskStatus = TaskStatus.TODO
    estimated_hours: float = 0.0
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None

class TaskCreate(TaskBase):
    goal_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority_score: Optional[float] = None
    status: Optional[TaskStatus] = None
    estimated_hours: Optional[float] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None

class TaskInDBBase(TaskBase):
    id: int
    goal_id: int

    class Config:
        from_attributes = True

class Task(TaskInDBBase):
    pass
