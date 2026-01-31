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
        team_data = payload.get("team", []) 
        
        logger.info(f"SchedulerAgent: Assigning {len(tasks)} tasks among {len(team_data)} team members.")

        # If no tasks, return early
        if not tasks:
            return {"tasks": []}

        scheduled_tasks = tasks  # Default to modification in place

        try:
            # 1. Attempt watsonx scheduling
            # Only try if we have team members
            if team_data:
                response = await watsonx_service.run_agent(
                    agent_id="orbit_scheduler_v1",
                    payload={"tasks": tasks, "team": team_data}
                )
                if "scheduled_tasks" in response and response["scheduled_tasks"]:
                    return {"tasks": response["scheduled_tasks"]}
            
        except Exception as e:
            logger.error(f"SchedulerAgent: watsonx call failed: {str(e)}")
            # Continue to fallback

        # 2. Smart assignment fallback (Skill-based matching)
        if not team_data:
            logger.warning("SchedulerAgent: No team members available for assignment.")
            for task in scheduled_tasks:
                task["assigned_to"] = None
                task["assigned_name"] = "Unassigned"
                task["estimated_hours"] = task.get("estimated_hours", 2.0)
            return {"tasks": scheduled_tasks}

        # Helper to score a member against a task
        def score_member(member, task):
            score = 0
            # text to search: title + description
            text = (task.get("title", "") + " " + task.get("description", "")).lower()
            
            skills = member.get("skills", {}) or {} # Handle None
            
            # 1. Skill Match Score
            for skill_name, skill_level in skills.items():
                if skill_name.lower() in text:
                    # deeply reward matching skills (level 1-5) * weight
                    score += (skill_level * 10)
            
            # 2. Workload Penalty (Small check to prefer available people)
            # Higher workload = lower score benefit
            workload = member.get("workload_score", 0.0)
            score -= (workload * 5)
            
            return score

        # Assign each task to the best fit
        for task in scheduled_tasks:
            # Sort candidates by Score (Desc), then Workload (Asc)
            # We shuffle slightly or just sort stable? stable sort is fine.
            # We use negative workload as tie breaker for descending sort if we wanted, 
            # but simpler to just calc a single float score.
            
            best_member = max(team_data, key=lambda m: score_member(m, task))
            
            task["assigned_to"] = best_member.get("id")
            task["assigned_name"] = best_member.get("name")
            
            # Dynamic estimate based on match? 
            # If score is high -> lower time? Keep it simple: 2.0
            task["estimated_hours"] = 2.0
            
            # Update member workload virtually to prevent overloading same person in one batch
            # (Simple greedy approach)
            best_member["workload_score"] = best_member.get("workload_score", 0.0) + 0.1

        return {"tasks": scheduled_tasks}

scheduler_agent = SchedulerAgent()
