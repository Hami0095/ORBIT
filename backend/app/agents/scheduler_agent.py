import logging
from typing import Dict, Any, List
from backend.app.agents.base_agent import BaseAgent
from backend.app.services.watsonx_service import watsonx_service

logger = logging.getLogger(__name__)

class SchedulerAgent(BaseAgent):
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedules tasks and assigns team members.
        Uses load-balancing logic (lowest workload score first).
        """
        tasks = payload.get("tasks", [])
        team_data = payload.get("team", []) # Expecting list of dicts/DTOs, not ORMs
        
        logger.info(f"SchedulerAgent: Assigning {len(tasks)} tasks among {len(team_data)} team members.")

        try:
            # 1. Attempt watsonx scheduling
            response = await watsonx_service.run_agent(
                agent_id="orbit_scheduler_v1",
                payload={"tasks": tasks, "team": team_data}
            )
            if "scheduled_tasks" in response:
                return {"tasks": response["scheduled_tasks"]}
        except Exception as e:
            logger.error(f"SchedulerAgent: watsonx call failed: {str(e)}")

        # 2. Smart assignment fallback
        # Sort team by workload_score ascending (lowest workload first)
        sorted_team = sorted(team_data, key=lambda x: x.get("workload_score", 0.0))
        
        for i, task in enumerate(tasks):
            if sorted_team:
                # Basic load balancer: pick one from the sorted list
                # For fallback, we cycle through them but prioritized by load
                member = sorted_team[i % len(sorted_team)]
                task["assigned_to"] = member.get("id")
                task["assigned_name"] = member.get("name")
            else:
                task["assigned_to"] = None
                
            task["estimated_hours"] = 2.0 # Default fallback estimate
            
        return {"tasks": tasks}

scheduler_agent = SchedulerAgent()
