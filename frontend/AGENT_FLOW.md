# ORBIT Agent Flow Integration Guide

This guide details how to integrate the backend AI agents into the frontend application.

## 1. Authentication (Updated)
The login endpoint has been updated to be Swagger/OAuth2 compatible.

- **Endpoint**: `POST /api/v1/auth/login/access-token`
- **Content-Type**: `application/x-www-form-urlencoded`
- **Body**:
  - `username`: User's email
  - `password`: User's password
- **Response**:
  ```json
  {
    "access_token": "eyJhbG...",
    "token_type": "bearer"
  }
  ```

## 2. Team Onboarding (Crucial!)
Before creating goals, the user **MUST** add team members. The Scheduler Agent needs a team to assign tasks to.

### Add Team Member
- **Endpoint**: `POST /api/v1/team/`
- **Body**:
  ```json
  {
    "name": "Sarah Jenkins",
    "skill_set": {
      "backend": 5,
      "python": 5,
      "postgres": 4
    },
    "availability_hours": 40
  }
  ```
- **Note**: `skill_set` is a dictionary of `Skill Name: Level (1-5)`. Key skills to include: "backend", "frontend", "react", "devops", "testing".

### List Team
- **Endpoint**: `GET /api/v1/team/`
- **Use**: Show the roster on the dashboard side panel.

## 3. Agent Orchestration Flow

The core workflow consists of **Goal Creation** -> **Orchestration** -> **Task Management**.

### Step 1: Create a Goal
First, the user defines what they want to achieve.

- **Endpoint**: `POST /api/v1/goals`
- **Body**:
  ```json
  {
    "title": "Migrate Legacy DB to Postgres",
    "description": "Migrate our old Oracle database to a new Postgres cluster on AWS, ensuring zero downtime and data integrity."
  }
  ```
- **Response**: Returns the created Goal object (take note of `id`).

### Step 2: Trigger the Agents
Call the orchestrator to have the AI agents break down the goal, prioritize tasks, and assign them to the team.

- **Endpoint**: `POST /api/v1/orchestrate/start/{goal_id}`
- **Method**: `POST`
- **Behavior**: This runs the following pipeline synchronously:
  1.  **Planner Agent**: Breaks goal into 5-6 logical phases (Analysis, Prep, Execution, Integration, Validation).
  2.  **Prioritizer Agent**: specialized AI scores tasks (0.0 - 1.0) based on urgency and impact.
  3.  **Scheduler Agent**: Assigns tasks to team members based on **skill matching** (e.g., "backend", "react") and workload availability.
  4.  **Executor/Insight Agents**: Finalize and summarize.

- **Response**:
  ```json
  {
    "status": "completed",
    "summary": "Generated 5 tasks covering analysis to deployment...",
    "task_count": 5,
    "metrics": { ... }
  }
  ```

### Step 3: Display Generated Tasks
Once orchestration is complete, fetch the newly generated tasks to display on the dashboard.

- **Endpoint**: `GET /api/v1/tasks?goal_id={goal_id}`
- **Response**: Array of Task objects.
- **Key Fields to Display**:
  - `title`: Task name (e.g., "Analyze: Postgres Migration")
  - `description`: Detailed instructions.
  - `assigned_to`: ID of the assigned team member.
  - `assigned_name`: Name of the assigned team member (Virtual field if populated, otherwise look up via Team API).
  - `priority_score`: Float (0.0-1.0). Use to color code (Red/High > 0.8, Yellow/Med > 0.5).
  - `status`: "TODO" (default).

## 4. Scheduling Logic
The Scheduler Agent uses team skills to make intelligent assignments.

- **Logic**:
  - Tasks with "backend", "database" -> Assigned to Backend Engineers.
  - Tasks with "ui", "frontend" -> Assigned to Frontend Engineers.
  - Fallback -> Assigned to member with lowest workload.

## Example Usage (React/TypeScript)

```typescript
// 1. Start Orchestration
const startOrchestration = async (goalId: number) => {
  setIsLoading(true);
  try {
    const res = await api.post(`/orchestrate/start/${goalId}`);
    if (res.data.status === 'completed') {
      // 2. Refresh Task List
      fetchTasks(goalId);
    }
  } catch (err) {
    console.error("Agent pipeline failed", err);
  } finally {
    setIsLoading(false);
  }
};
```
