import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.agents.planner_agent import planner_agent
from backend.app.agents.prioritizer_agent import prioritizer_agent
from backend.app.agents.scheduler_agent import scheduler_agent
from backend.app.agents.executor_agent import executor_agent
from backend.app.agents.insight_agent import insight_agent
from backend.app.repositories.agent_log_repository import agent_log_repo
from backend.app.repositories.task_repository import task_repo
from backend.app.repositories.team_repository import team_repo
from backend.app.repositories.goal_repository import goal_repo
from backend.app.schemas.task import TaskCreate
from backend.app.db.models import GoalStatus

logger = logging.getLogger(__name__)

class OrbitOrchestrator:
    """
    Main orchestrator for the ORBIT AI Agent pipeline.
    Implements a robust sequential pipeline logic with shared context and error handling.
    """

    async def orchestrate(self, db: AsyncSession, goal_id: int, goal_text: str) -> Dict[str, Any]:
        logger.info(f"Orchestrator: Initializing pipeline for Goal ID: {goal_id}")

        # 0. Context & State Initialization with Date Awareness
        today = datetime.now()
        
        # Calculate days until Friday (4 = Friday in weekday())
        days_until_friday = (4 - today.weekday()) % 7
        # If today is Friday or later in the week, target next Friday
        if days_until_friday == 0 and today.weekday() == 4:
            # Today is Friday, target this Friday
            end_of_week = today
        elif today.weekday() >= 4:
            # Saturday or Sunday, target next Friday
            end_of_week = today + timedelta(days=(4 - today.weekday() + 7))
        else:
            # Monday-Thursday, target this Friday
            end_of_week = today + timedelta(days=days_until_friday)
        
        context = {
            "goal_id": goal_id,
            "goal_text": goal_text,
            "start_date": today.strftime("%Y-%m-%d"),
            "end_date": end_of_week.strftime("%Y-%m-%d"),
            "week_description": f"Week of {today.strftime('%B %d')} to {end_of_week.strftime('%B %d, %Y')}",
            "tasks": [],
            "execution": {},
            "insight": {},
            "errors": []
        }
        
        logger.info(f"Orchestrator: Planning for {context['week_description']}")

        # Retrieve goal object for status updates
        goal = await goal_repo.get(db, id=goal_id)
        if not goal:
            return {"status": "error", "message": "Goal not found."}

        # Set initial status
        await goal_repo.update(db, db_obj=goal, obj_in={"status": GoalStatus.IN_PROGRESS})

        try:
            # 1. Pipeline Stages
            await self._run_planner_stage(db, context)
            await self._run_prioritizer_stage(db, context)
            await self._run_scheduler_stage(db, context)
            
            # Persist tasks before execution
            await self._persist_tasks(db, context)
            
            await self._run_executor_stage(db, context)
            await self._run_insight_stage(db, context)

            # 2. Finalize Success
            await goal_repo.update(db, db_obj=goal, obj_in={"status": GoalStatus.COMPLETED})
            
            return {
                "status": "completed",
                "summary": context["insight"].get("summary"),
                "metrics": context["insight"].get("metrics", {}),
                "task_count": len(context["tasks"]),
                "integrations_triggered": context["execution"].get("actions", []),
                "next_steps": context["insight"].get("next_steps")
            }

        except Exception as e:
            import sys
            print(f"CRITICAL ERROR: {e}", file=sys.stderr)
            logger.error(f"Orchestrator: Pipeline failure - {str(e)}")
            await goal_repo.update(db, db_obj=goal, obj_in={"status": GoalStatus.FAILED})
            return {
                "status": "failed",
                "error": str(e),
                "stage": context.get("current_stage", "initialization")
            }

    async def _run_planner_stage(self, db: AsyncSession, context: Dict[str, Any]):
        context["current_stage"] = "Planning"
        logger.debug("Orchestrator Stage: Planning")
        output = await planner_agent.run({
            "goal_text": context["goal_text"],
            "start_date": context["start_date"],
            "end_date": context["end_date"],
            "week_description": context["week_description"]
        })
        context["tasks"] = output.get("tasks", [])
        await agent_log_repo.create(db, agent_name="Planner", action="plan", payload=output)

    async def _run_prioritizer_stage(self, db: AsyncSession, context: Dict[str, Any]):
        context["current_stage"] = "Prioritization"
        logger.debug("Orchestrator Stage: Prioritization")
        output = await prioritizer_agent.run({
            "tasks": context["tasks"], 
            "goal_text": context["goal_text"]
        })
        context["tasks"] = output.get("tasks", [])
        await agent_log_repo.create(db, agent_name="Prioritizer", action="prioritize", payload=output)

    async def _run_scheduler_stage(self, db: AsyncSession, context: Dict[str, Any]):
        context["current_stage"] = "Scheduling"
        logger.debug("Orchestrator Stage: Scheduling")
        
        # Convert ORM team members to plain dict DTOs for the agent
        team_members = await team_repo.get_multi(db)
        team_dtos = [
            {
                "id": m.id, 
                "name": m.name, 
                "skills": m.skill_set, 
                "availability_hours": m.availability_hours,
                "workload_score": m.workload_score if hasattr(m, "workload_score") else 0.0
            }
            for m in team_members
        ]
        
        output = await scheduler_agent.run({
            "tasks": context["tasks"],
            "team": team_dtos
        })
        context["tasks"] = output.get("tasks", [])
        await agent_log_repo.create(db, agent_name="Scheduler", action="schedule", payload=output)

    async def _persist_tasks(self, db: AsyncSession, context: Dict[str, Any]):
        logger.debug("Orchestrator: Persisting tasks to database")
        for task_data in context["tasks"]:
            # Parse due_date if it exists in task_data
            due_date = None
            if task_data.get("due_date"):
                try:
                    due_date = datetime.fromisoformat(task_data["due_date"])
                except Exception:
                    # Fallback to end_date if parsing fails
                    due_date = datetime.fromisoformat(context["end_date"])

            task_in = TaskCreate(
                goal_id=context["goal_id"],
                title=task_data["title"],
                description=task_data["description"],
                priority_score=task_data.get("priority_score", 0.0),
                assigned_to=task_data.get("assigned_to"),
                estimated_hours=task_data.get("estimated_hours", 0.0),
                due_date=due_date
            )
            await task_repo.create(db, obj_in=task_in)

    async def _run_executor_stage(self, db: AsyncSession, context: Dict[str, Any]):
        context["current_stage"] = "Execution"
        logger.debug("Orchestrator Stage: Execution")
        output = await executor_agent.run({"tasks": context["tasks"]})
        context["execution"] = output
        await agent_log_repo.create(db, agent_name="Executor", action="execute", payload=output)

    async def _run_insight_stage(self, db: AsyncSession, context: Dict[str, Any]):
        context["current_stage"] = "Insight"
        logger.debug("Orchestrator Stage: Insight")
        output = await insight_agent.run({
            "tasks": context["tasks"],
            "execution": context["execution"]
        })
        context["insight"] = output
        await agent_log_repo.create(db, agent_name="Insight", action="summarize", payload=output)

orbit_orchestrator = OrbitOrchestrator()
