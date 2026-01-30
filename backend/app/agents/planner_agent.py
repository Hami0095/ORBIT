from typing import Dict, Any
from backend.app.agents.base_agent import BaseAgent
from backend.app.services.watsonx_service import watsonx_service

class PlannerAgent(BaseAgent):
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Breaks goals into tasks.
        """
        # In the future, this calls a specific watsonx skill/agent
        response = await watsonx_service.run_agent("planner_id", payload)
        
        # Mocking task breakdown logic
        goal_text = payload.get("goal_text", "")
        tasks = [
            {"title": f"Task 1 for: {goal_text}", "description": "Auto-generated step 1"},
            {"title": f"Task 2 for: {goal_text}", "description": "Auto-generated step 2"}
        ]
        return {"tasks": tasks}

planner_agent = PlannerAgent()
