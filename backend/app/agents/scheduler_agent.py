from typing import Dict, Any
from backend.app.agents.base_agent import BaseAgent
from backend.app.services.watsonx_service import watsonx_service

class SchedulerAgent(BaseAgent):
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedules tasks and assigns team members.
        """
        response = await watsonx_service.run_agent("scheduler_id", payload)
        
        tasks = payload.get("tasks", [])
        team = payload.get("team", [])
        
        for i, task in enumerate(tasks):
            if team:
                task["assigned_to"] = team[i % len(team)].id
            task["estimated_hours"] = 2.0
            
        return {"tasks": tasks}

scheduler_agent = SchedulerAgent()
