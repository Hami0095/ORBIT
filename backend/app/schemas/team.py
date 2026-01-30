from pydantic import BaseModel
from typing import Optional, Dict

class TeamMemberBase(BaseModel):
    name: str
    skill_set: Dict[str, int]
    availability_hours: int = 40

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMemberUpdate(BaseModel):
    name: Optional[str] = None
    skill_set: Optional[Dict[str, int]] = None
    availability_hours: Optional[int] = None
    workload_score: Optional[float] = None

class TeamMemberInDBBase(TeamMemberBase):
    id: int
    workload_score: float

    class Config:
        from_attributes = True

class TeamMember(TeamMemberInDBBase):
    pass
