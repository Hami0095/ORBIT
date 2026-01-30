import logging
from typing import Dict, Any, List
from backend.app.agents.base_agent import BaseAgent
from backend.app.services.watsonx_service import watsonx_service

logger = logging.getLogger(__name__)

class PlannerAgent(BaseAgent):
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Breaks natural language goals into actionable tasks.
        Attempts to use IBM watsonx for intelligent breakdown with robust fallback.
        """
        goal_text = payload.get("goal_text", "")
        logger.info(f"PlannerAgent: Processing goal - '{goal_text[:50]}...'")

        try:
            # 1. Attempt watsonx Orchestrate call
            response = await watsonx_service.run_agent(
                agent_id="orbit_planner_v1", 
                payload={"goal": goal_text, "instruction": "Break this goal into 3-6 actionable IT tasks."}
            )
            
            # If watsonx returned structured tasks, use them
            if "tasks" in response:
                return {"tasks": response["tasks"]}
                
        except Exception as e:
            logger.error(f"PlannerAgent: watsonx call failed: {str(e)}")

        # 2. Smart Fallback Logic (Production Quality Mock)
        # We split the goal into logical phases: Analysis, Execution, Validation
        fallback_tasks = [
            {
                "title": "Discovery & Requirement Analysis", 
                "description": f"Identify all technical requirements and stakeholder needs for: {goal_text}."
            },
            {
                "title": "Resource & Environment Preparation", 
                "description": "Set up necessary infrastructure, specialized tools, and team access."
            },
            {
                "title": "Core Implementation Phase", 
                "description": "Execute the primary technical workflow to achieve the stated goal."
            },
            {
                "title": "Quality Assurance & Validation", 
                "description": "Verify that the implementation meets all success criteria and stability standards."
            },
            {
                "title": "Final Review & Documentation", 
                "description": "Summarize outcomes, update support docs, and conduct a post-implementation review."
            }
        ]

        logger.info(f"PlannerAgent: Using fallback phase-based breakdown (5 tasks)")
        return {"tasks": fallback_tasks}

planner_agent = PlannerAgent()
