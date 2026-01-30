import logging
from typing import Dict, Any
from backend.app.agents.base_agent import BaseAgent
from backend.app.services.watsonx_service import watsonx_service

logger = logging.getLogger(__name__)

class PrioritizerAgent(BaseAgent):
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assigns priority scores (0.0 to 1.0) to tasks.
        Detects urgency from goal context and task descriptions.
        """
        tasks = payload.get("tasks", [])
        goal_text = payload.get("goal_text", "").lower()
        
        logger.info(f"PrioritizerAgent: Scoring {len(tasks)} tasks.")

        try:
            # 1. Attempt watsonx scoring
            response = await watsonx_service.run_agent(
                agent_id="orbit_prioritizer_v1",
                payload={"tasks": tasks, "goal_context": goal_text}
            )
            if "scored_tasks" in response:
                return {"tasks": response["scored_tasks"]}
        except Exception as e:
            logger.error(f"PrioritizerAgent: watsonx call failed: {str(e)}")

        # 2. Smart scoring fallback
        # Check for urgency signals
        urgency_keywords = ["urgent", "critical", "outage", "emergency", "blocker", "p0", "p1"]
        is_urgent = any(kw in goal_text for kw in urgency_keywords)
        
        base_multiplier = 0.9 if is_urgent else 0.6
        
        for i, task in enumerate(tasks):
            # Tasks are usually generated in logical order, 
            # so we slightly decay the score, but keep it high if the goal is urgent
            raw_score = base_multiplier - (i * 0.1)
            # Ensure score is normalized within 0.0 - 1.0
            task["priority_score"] = max(0.1, min(1.0, round(raw_score, 2)))
            
        return {"tasks": tasks}

prioritizer_agent = PrioritizerAgent()
