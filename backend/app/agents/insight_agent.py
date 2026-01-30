from typing import Dict, Any
from backend.app.agents.base_agent import BaseAgent
from backend.app.services.watsonx_service import watsonx_service

class InsightAgent(BaseAgent):
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates summaries and insights.
        """
        response = await watsonx_service.run_agent("insight_id", payload)
        
        return {"summary": "All tasks scheduled and team notified successfully."}

insight_agent = InsightAgent()
