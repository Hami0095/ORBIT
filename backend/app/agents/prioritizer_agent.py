from typing import Dict, Any
from backend.app.agents.base_agent import BaseAgent
from backend.app.services.watsonx_service import watsonx_service

class PrioritizerAgent(BaseAgent):
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prioritizes tasks.
        """
        response = await watsonx_service.run_agent("prioritizer_id", payload)
        
        tasks = payload.get("tasks", [])
        for i, task in enumerate(tasks):
            task["priority_score"] = 0.9 - (i * 0.1)
            
        return {"tasks": tasks}

prioritizer_agent = PrioritizerAgent()
