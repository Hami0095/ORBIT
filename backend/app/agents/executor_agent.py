import logging
from typing import Dict, Any, List
from backend.app.agents.base_agent import BaseAgent
from backend.app.services.watsonx_service import watsonx_service

logger = logging.getLogger(__name__)

class ExecutorAgent(BaseAgent):
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinates execution by identifying required external integrations.
        Returns a structured list of 'actions' to be performed.
        """
        tasks = payload.get("tasks", [])
        logger.info(f"ExecutorAgent: Analyzing execution requirements for {len(tasks)} tasks.")

        try:
            # 1. Attempt watsonx tool selection
            response = await watsonx_service.run_agent(
                agent_id="orbit_executor_v1",
                payload={"tasks": tasks}
            )
            if "actions" in response:
                return {"actions": response["actions"]}
        except Exception as e:
            logger.error(f"ExecutorAgent: watsonx call failed: {str(e)}")

        # 2. Smart integration mapping fallback
        # Instead of just finding words, we map task intent to known tools
        actions = []
        
        tool_mapping = {
            "slack": ["notif", "update", "slack", "message", "alert", "notify"],
            "jira": ["ticket", "jira", "issue", "bug", "task", "backlog"],
            "email": ["email", "send", "report", "stakeholder"],
            "calendar": ["meeting", "schedule", "calendar", "invite"]
        }

        for task in tasks:
            text = (task.get("title", "") + " " + task.get("description", "")).lower()
            
            for tool, keywords in tool_mapping.items():
                if any(kw in text for kw in keywords):
                    actions.append(f"trigger_{tool}")

        # Unique actions only, with a default if none found
        unique_actions = list(set(actions))
        if not unique_actions:
            unique_actions = ["internal_log_update"]
            
        return {
            "actions": unique_actions,
            "status": "triggered",
            "execution_timestamp": "2026-01-31T01:35:00Z"
        }

executor_agent = ExecutorAgent()
