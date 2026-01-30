from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models here for Alembic
from backend.app.db.models import User, TeamMember, Goal, Task, Schedule, AgentLog, Integration # noqa
