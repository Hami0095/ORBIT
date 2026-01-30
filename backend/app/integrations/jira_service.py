import logging

logger = logging.getLogger(__name__)

class JiraService:
    async def create_issue(self, project: str, summary: str, description: str) -> str:
        issue_id = f"ORB-{123}"
        logger.info(f"MOCK: Creating Jira issue in {project}: {summary}")
        return issue_id

jira_service = JiraService()
