from backend.app.repositories.base import BaseRepository
from backend.app.db.models import TeamMember
from backend.app.schemas.team import TeamMemberCreate, TeamMemberUpdate

class TeamRepository(BaseRepository[TeamMember, TeamMemberCreate, TeamMemberUpdate]):
    pass

team_repo = TeamRepository(TeamMember)
