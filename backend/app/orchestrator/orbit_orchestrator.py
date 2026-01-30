import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.agents.planner_agent import planner_agent
from backend.app.agents.prioritizer_agent import prioritizer_agent
from backend.app.agents.scheduler_agent import scheduler_agent
from backend.app.agents.executor_agent import executor_agent
from backend.app.agents.insight_agent import insight_agent
from backend.app.repositories.agent_log_repository import agent_log_repo
from backend.app.repositories.task_repository import task_repo
from backend.app.repositories.team_repository import team_repo
from backend.app.schemas.task import TaskCreate

logger = logging.getLogger(__name__)

class OrbitOrchestrator:
    async def orchestrate(self, db: AsyncSession, goal_id: int, goal_text: str) -> Dict[str, Any]:
        logger.info(f"Starting orchestration for Goal ID: {goal_id}")
        
        # 1. Planning
        plan_output = await planner_agent.run({"goal_text": goal_text})
        await agent_log_repo.create(db, agent_name="Planner", action="plan", payload=plan_output)
        
        # 2. Prioritization
        prio_output = await prioritizer_agent.run({"tasks": plan_output["tasks"]})
        await agent_log_repo.create(db, agent_name="Prioritizer", action="prioritize", payload=prio_output)
        
        # 3. Scheduling
        team_members = await team_repo.get_multi(db)
        schedule_output = await scheduler_agent.run({
            "tasks": prio_output["tasks"],
            "team": team_members
        })
        await agent_log_repo.create(db, agent_name="Scheduler", action="schedule", payload=schedule_output)
        
        # Save tasks to DB
        for task_data in schedule_output["tasks"]:
            task_in = TaskCreate(
                goal_id=goal_id,
                title=task_data["title"],
                description=task_data["description"],
                priority_score=task_data.get("priority_score", 0.0),
                assigned_to=task_data.get("assigned_to"),
                estimated_hours=task_data.get("estimated_hours", 0.0)
            )
            await task_repo.create(db, obj_in=task_in)
            
        # 4. Execution (External Tools)
        exec_output = await executor_agent.run({"tasks": schedule_output["tasks"]})
        await agent_log_repo.create(db, agent_name="Executor", action="execute", payload=exec_output)
        
        # 5. Insight
        insight_output = await insight_agent.run({"execution": exec_output})
        await agent_log_repo.create(db, agent_name="Insight", action="summarize", payload=insight_output)
        
        return {
            "status": "completed",
            "summary": insight_output["summary"],
            "task_count": len(schedule_output["tasks"])
        }

orbit_orchestrator = OrbitOrchestrator()
