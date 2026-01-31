import pytest
from backend.app.agents.planner_agent import planner_agent
from backend.app.agents.prioritizer_agent import prioritizer_agent
from backend.app.agents.scheduler_agent import scheduler_agent
from backend.app.agents.executor_agent import executor_agent
from backend.app.agents.insight_agent import insight_agent

@pytest.mark.asyncio
async def test_planner_agent_returns_tasks(mock_watsonx):
    """Test that PlannerAgent returns a list of tasks."""
    payload = {"goal_text": "Deploy new microservice to production"}
    result = await planner_agent.run(payload)
    
    assert "tasks" in result
    assert isinstance(result["tasks"], list)
    assert len(result["tasks"]) > 0
    
    # Verify task structure
    for task in result["tasks"]:
        assert "title" in task
        assert "description" in task
        assert isinstance(task["title"], str)
        assert isinstance(task["description"], str)

@pytest.mark.asyncio
async def test_planner_agent_with_empty_goal(mock_watsonx):
    """Test PlannerAgent handles empty goal gracefully."""
    payload = {"goal_text": ""}
    result = await planner_agent.run(payload)
    
    assert "tasks" in result
    assert isinstance(result["tasks"], list)
    # Should still return fallback tasks
    assert len(result["tasks"]) > 0

@pytest.mark.asyncio
async def test_planner_agent_with_long_complex_goal(mock_watsonx):
    """Test PlannerAgent handles messy manager input."""
    payload = {
        "goal_text": "We need to urgently fix the database outage issue that's affecting "
                     "production and also migrate to the new cloud infrastructure while "
                     "ensuring zero downtime and coordinating with 5 different teams..."
    }
    result = await planner_agent.run(payload)
    
    assert "tasks" in result
    assert len(result["tasks"]) > 0

@pytest.mark.asyncio
async def test_prioritizer_agent_assigns_scores(mock_watsonx):
    """Test that PrioritizerAgent assigns priority_score to tasks."""
    tasks = [
        {"title": "Task 1", "description": "Normal task"},
        {"title": "Task 2", "description": "Another task"},
    ]
    payload = {"tasks": tasks, "goal_text": "regular goal"}
    result = await prioritizer_agent.run(payload)
    
    assert "tasks" in result
    assert len(result["tasks"]) == 2
    
    for task in result["tasks"]:
        assert "priority_score" in task
        assert isinstance(task["priority_score"], (int, float))
        assert 0.0 <= task["priority_score"] <= 1.0

@pytest.mark.asyncio
async def test_prioritizer_agent_urgent_detection(mock_watsonx):
    """Test PrioritizerAgent detects urgency and applies higher scores."""
    tasks = [
        {"title": "Task 1", "description": "Fix critical outage"},
    ]
    payload = {"tasks": tasks, "goal_text": "urgent critical P0 emergency"}
    result = await prioritizer_agent.run(payload)
    
    # Urgent tasks should have higher scores
    assert result["tasks"][0]["priority_score"] >= 0.7

@pytest.mark.asyncio
async def test_scheduler_agent_assigns_team_members(mock_watsonx):
    """Test that SchedulerAgent assigns team members to tasks."""
    tasks = [
        {"title": "Task 1", "description": "Deploy service"},
        {"title": "Task 2", "description": "Run tests"},
    ]
    team = [
        {"id": 1, "name": "Alice", "role": "DevOps", "workload_score": 0.3},
        {"id": 2, "name": "Bob", "role": "Backend", "workload_score": 0.5},
    ]
    payload = {"tasks": tasks, "team": team}
    result = await scheduler_agent.run(payload)
    
    assert "tasks" in result
    for task in result["tasks"]:
        assert "assigned_to" in task
        assert "estimated_hours" in task

@pytest.mark.asyncio
async def test_scheduler_agent_with_no_team(mock_watsonx):
    """Test SchedulerAgent handles empty team list."""
    tasks = [{"title": "Task 1", "description": "Deploy"}]
    payload = {"tasks": tasks, "team": []}
    result = await scheduler_agent.run(payload)
    
    assert "tasks" in result
    assert result["tasks"][0]["assigned_to"] is None

@pytest.mark.asyncio
async def test_executor_agent_returns_actions(mock_watsonx):
    """Test that ExecutorAgent returns integration actions."""
    tasks = [
        {"title": "Send Slack notification", "description": "Notify team on Slack"},
        {"title": "Create Jira ticket", "description": "Track issue in Jira"},
    ]
    payload = {"tasks": tasks}
    result = await executor_agent.run(payload)
    
    assert "actions" in result
    assert isinstance(result["actions"], list)
    assert len(result["actions"]) > 0

@pytest.mark.asyncio
async def test_executor_agent_maps_integrations(mock_watsonx):
    """Test ExecutorAgent correctly maps task keywords to tools."""
    tasks = [
        {"title": "Slack update", "description": "Send message to channel"},
    ]
    payload = {"tasks": tasks}
    result = await executor_agent.run(payload)
    
    # Should trigger slack
    assert any("slack" in action.lower() for action in result["actions"])

@pytest.mark.asyncio
async def test_insight_agent_returns_summary(mock_watsonx):
    """Test that InsightAgent returns comprehensive analytics."""
    tasks = [
        {"title": "Task 1", "description": "Do something", "priority_score": 0.8},
        {"title": "Task 2", "description": "Do more", "priority_score": 0.6},
    ]
    execution = {"actions": ["trigger_slack", "trigger_jira"]}
    payload = {"tasks": tasks, "execution": execution}
    result = await insight_agent.run(payload)
    
    assert "summary" in result
    assert "metrics" in result
    assert isinstance(result["summary"], str)
    assert len(result["summary"]) > 0
    
    # Check metrics
    metrics = result["metrics"]
    assert "task_count" in metrics
    assert "integration_count" in metrics
    assert "risk_score" in metrics
    assert metrics["task_count"] == 2
    assert metrics["integration_count"] == 2
