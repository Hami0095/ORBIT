from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from backend.app.db.base import Base

class UserRole(str, enum.Enum):
    MANAGER = "MANAGER"

class GoalStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    BLOCKED = "BLOCKED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.MANAGER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    skill_set = Column(JSON)  # e.g., {"python": 5, "devops": 4}
    availability_hours = Column(Integer, default=40)
    workload_score = Column(Float, default=0.0)
    manager_id = Column(Integer, ForeignKey("users.id"))

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(Enum(GoalStatus), default=GoalStatus.PENDING)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("Task", back_populates="goal")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    title = Column(String, index=True)
    description = Column(String)
    priority_score = Column(Float, default=0.0)
    assigned_to = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    estimated_hours = Column(Float, default=0.0)
    due_date = Column(DateTime(timezone=True), nullable=True)

    goal = relationship("Goal", back_populates="tasks")
    schedules = relationship("Schedule", back_populates="task")

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))

    task = relationship("Task", back_populates="schedules")

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String)
    action = Column(String)
    payload_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # slack, jira, etc.
    credentials_json = Column(JSON)
