import pytest
from backend.app.orchestrator.orbit_orchestrator import orbit_orchestrator
from backend.app.repositories.goal_repository import goal_repo
from backend.app.repositories.task_repository import task_repo
from backend.app.repositories.team_repository import team_repo
from backend.app.schemas.goal import GoalCreate
from backend.app.schemas.team import TeamMemberCreate
from backend.app.db.models import GoalStatus

@pytest.mark.asyncio
async def test_orchestrator_full_pipeline_success(test_db, mock_watsonx):
    """Test complete orchestration pipeline executes successfully."""
    # Create a goal
    goal_in = GoalCreate(
        title="Deploy to production",
        description="Deploy new microservice",
        created_by=1
    )
    goal = await goal_repo.create_with_owner(test_db, obj_in=goal_in, owner_id=1)
    
    # Create team members
    team1 = TeamMemberCreate(name="Alice", skill_set={"python": 5})
    team2 = TeamMemberCreate(name="Bob", skill_set={"devops": 4})
    await team_repo.create(test_db, obj_in=team1)
    await team_repo.create(test_db, obj_in=team2)
    
    # Run orchestration
    result = await orbit_orchestrator.orchestrate(
        db=test_db,
        goal_id=goal.id,
        goal_text=goal.description
    )
    
    # Verify result
    if result["status"] != "completed":
        import sys
        print(f"DEBUG: Pipeline failed with error: {result.get('error')}", file=sys.stderr)
    assert result["status"] == "completed"
    assert "summary" in result
    assert "task_count" in result
    assert result["task_count"] > 0
    assert "integrations_triggered" in result
    
    # Verify goal status updated
    updated_goal = await goal_repo.get(test_db, id=goal.id)
    assert updated_goal.status == GoalStatus.COMPLETED
    
    # Verify tasks were persisted
    tasks = await task_repo.get_multi_by_goal(test_db, goal_id=goal.id)
    assert len(tasks) == result["task_count"]

@pytest.mark.asyncio
async def test_orchestrator_with_messy_long_input(test_db, mock_watsonx):
    """Test orchestrator handles complex manager input."""
    goal_in = GoalCreate(
        title="Complex IT Project",
        description="We urgently need to migrate the entire legacy database infrastructure "
                    "to AWS cloud while maintaining 99.99% uptime and coordinating between "
                    "DevOps, Backend, Frontend, QA, and Security teams, also need to ensure "
                    "compliance with GDPR and SOC2 requirements...",
        created_by=1
    )
    goal = await goal_repo.create_with_owner(test_db, obj_in=goal_in, owner_id=1)
    
    # Create a team member
    team = TeamMemberCreate(name="Charlie", skill_set={"cloud": 5})
    await team_repo.create(test_db, obj_in=team)
    
    result = await orbit_orchestrator.orchestrate(
        db=test_db,
        goal_id=goal.id,
        goal_text=goal.description
    )
    
    assert result["status"] == "completed"
    assert result["task_count"] > 0

@pytest.mark.asyncio
async def test_orchestrator_with_empty_goal_text(test_db, mock_watsonx):
    """Test orchestrator handles empty goal description."""
    goal_in = GoalCreate(
        title="Empty Goal",
        description="",
        created_by=1
    )
    goal = await goal_repo.create_with_owner(test_db, obj_in=goal_in, owner_id=1)
    
    result = await orbit_orchestrator.orchestrate(
        db=test_db,
        goal_id=goal.id,
        goal_text=goal.description
    )
    
    # Should still complete with fallback logic
    assert result["status"] == "completed"
    assert result["task_count"] > 0

@pytest.mark.asyncio
async def test_orchestrator_with_no_team_members(test_db, mock_watsonx):
    """Test orchestrator works when no team members exist."""
    goal_in = GoalCreate(
        title="Solo Project",
        description="Individual task with no team",
        created_by=1
    )
    goal = await goal_repo.create_with_owner(test_db, obj_in=goal_in, owner_id=1)
    
    # Don't create any team members
    result = await orbit_orchestrator.orchestrate(
        db=test_db,
        goal_id=goal.id,
        goal_text=goal.description
    )
    
    assert result["status"] == "completed"
    # Tasks should still be created but with no assignment
    tasks = await task_repo.get_multi_by_goal(test_db, goal_id=goal.id)
    assert len(tasks) > 0
    assert tasks[0].assigned_to is None

@pytest.mark.asyncio
async def test_orchestrator_agent_failure_handling(test_db, mocker):
    """Test orchestrator marks goal as FAILED when agent fails."""
    # Mock planner to fail - target the instance imported in the orchestrator
    mocker.patch(
        "backend.app.orchestrator.orbit_orchestrator.planner_agent.run",
        side_effect=Exception("Simulated agent failure")
    )
    
    goal_in = GoalCreate(
        title="Failing Goal",
        description="This will trigger a failure",
        created_by=1
    )
    goal = await goal_repo.create_with_owner(test_db, obj_in=goal_in, owner_id=1)
    
    result = await orbit_orchestrator.orchestrate(
        db=test_db,
        goal_id=goal.id,
        goal_text=goal.description
    )
    
    # Verify failure was handled
    assert result["status"] == "failed"
    assert "error" in result
    
    # Verify goal status set to FAILED
    updated_goal = await goal_repo.get(test_db, id=goal.id)
    assert updated_goal.status == GoalStatus.FAILED

@pytest.mark.asyncio
async def test_orchestrator_tasks_persisted_correctly(test_db, mock_watsonx):
    """Test that tasks are persisted with correct attributes."""
    goal_in = GoalCreate(
        title="Persistence Test",
        description="Verify task persistence",
        created_by=1
    )
    goal = await goal_repo.create_with_owner(test_db, obj_in=goal_in, owner_id=1)
    
    team = TeamMemberCreate(name="Dave", skill_set={"backend": 5})
    created_team = await team_repo.create(test_db, obj_in=team)
    
    result = await orbit_orchestrator.orchestrate(
        db=test_db,
        goal_id=goal.id,
        goal_text=goal.description
    )
    
    # Retrieve persisted tasks
    tasks = await task_repo.get_multi_by_goal(test_db, goal_id=goal.id)
    
    # Verify task attributes
    for task in tasks:
        assert task.goal_id == goal.id
        assert task.goal_id == goal.id
        assert task.title is not None
        assert task.description is not None
        assert task.priority_score >= 0.0
        assert task.estimated_hours > 0.0
        # At least some tasks should be assigned
    
    assert any(t.assigned_to == created_team.id for t in tasks)

@pytest.mark.asyncio
async def test_orchestrator_goal_status_transitions(test_db, mock_watsonx):
    """Test goal status transitions through the pipeline."""
    goal_in = GoalCreate(
        title="Status Test",
        description="Track status changes",
        created_by=1
    )
    goal = await goal_repo.create_with_owner(test_db, obj_in=goal_in, owner_id=1)
    
    # Initial status should be PENDING
    assert goal.status == GoalStatus.PENDING
    
    await orbit_orchestrator.orchestrate(
        db=test_db,
        goal_id=goal.id,
        goal_text=goal.description
    )
    
    # After orchestration, should be COMPLETED
    updated_goal = await goal_repo.get(test_db, id=goal.id)
    assert updated_goal.status == GoalStatus.COMPLETED
