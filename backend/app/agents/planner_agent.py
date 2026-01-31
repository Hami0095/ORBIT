import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from backend.app.agents.base_agent import BaseAgent
from backend.app.services.watsonx_service import watsonx_service

logger = logging.getLogger(__name__)

class PlannerAgent(BaseAgent):
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Breaks natural language goals into actionable tasks.
        Attempts to use IBM watsonx for intelligent breakdown with robust fallback.
        Now date-aware: tasks are planned for the current week (start_date to end_date).
        """
        goal_text = payload.get("goal_text", "")
        start_date = payload.get("start_date", "")
        end_date = payload.get("end_date", "")
        week_description = payload.get("week_description", "this week")
        
        logger.info(f"PlannerAgent: Processing goal - '{goal_text[:50]}...'")
        logger.info(f"PlannerAgent: Planning for {week_description}")

        try:
            # 1. Attempt watsonx Orchestrate call with date context
            response = await watsonx_service.run_agent(
                agent_id="orbit_planner_v1", 
                payload={
                    "goal": goal_text, 
                    "instruction": f"Break this goal into 3-6 actionable IT tasks to be completed between {start_date} and {end_date}.",
                    "start_date": start_date,
                    "end_date": end_date
                }
            )
            
            # If watsonx returned structured tasks, use them
            if "tasks" in response:
                return {"tasks": response["tasks"]}
                
        except Exception as e:
            logger.error(f"PlannerAgent: watsonx call failed: {str(e)}")

        # 2. Smart Fallback Logic (Production Quality Mock)
        # We split the goal into logical phases: Analysis, Execution, Validation
        logger.info(f"PlannerAgent: Using smart phase-based breakdown for goal: '{goal_text[:30]}...'")
        
        # Clean up goal text for titles (remove trailing dots, capitialize)
        short_goal = goal_text.split(".")[0].strip()
        if len(short_goal) > 40:
             short_goal = short_goal[:37] + "..."
             
        # Distribute tasks across the week
        t_start = datetime.fromisoformat(start_date)
        t_end = datetime.fromisoformat(end_date)
        delta = (t_end - t_start).days
        
        def calculate_due(day_offset):
            # Ensure we don't exceed the end date
            target_day = t_start + timedelta(days=min(day_offset, delta))
            return target_day.strftime("%Y-%m-%d")

        fallback_tasks = [
            {
                "title": f"Analyze: {short_goal}", 
                "description": f"Conduct initial requirement gathering and stakeholder analysis for '{goal_text}'. Identify success metrics and key risks. Timeline: {week_description}.",
                "due_date": calculate_due(1) # Usually Day 1 or 2
            },
            {
                "title": "Prepare Infrastructure & Backlog", 
                "description": f"Set up development environments, repositories, and define the detailed sprint backlog items for the week ({start_date} to {end_date}).",
                "due_date": calculate_due(2)
            },
            {
                "title": f"Execute Core Development: {short_goal}", 
                "description": f"Implement the primary business logic and core functionality required to achieve the goal. Target completion by {end_date}.",
                "due_date": calculate_due(4)
            },
            {
                "title": "Integrate Components & APIs", 
                "description": f"Connect frontend, backend, and external services. Ensure data flow is correct and secure. Scheduled for {week_description}.",
                "due_date": calculate_due(5)
            },
            {
                "title": "Validate Quality & Security", 
                "description": f"Run comprehensive unit, integration, and security tests. verify compliance with standards. Complete before {end_date}.",
                "due_date": calculate_due(6) if delta >= 6 else calculate_due(delta)
            },
            {
                "title": "Final Report & Deployment", 
                "description": f"Generate execution report, document the solution, and perform final deployment/handover by end of week ({end_date}).",
                "due_date": end_date
            }
        ]

        return {"tasks": fallback_tasks}

planner_agent = PlannerAgent()
