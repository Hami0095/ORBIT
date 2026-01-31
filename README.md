# ORBIT – AI Task Orchestrator (Backend)

ORBIT is an AI-powered task orchestration system designed for IT teams. It uses IBM watsonx Orchestrate agents to break down natural language goals into actionable tasks, prioritize them, and assign them to team members.

## Tech Stack

*   **Python 3.11+**
*   **FastAPI** (Async API)
*   **PostgreSQL** (Database)
*   **SQLAlchemy ORM** (Database interaction)
*   **Alembic** (Migrations)
*   **Pydantic** (Data validation)
*   **Docker & Docker Compose**

## Folder Structure

```
/backend
  /app
    main.py           # Entry point
    /core             # Config and Security
    /db               # Models, Sessions, Migrations
    /schemas          # Pydantic models
    /api              # FastAPI routes
    /services         # Business logic & watsonx integration
    /agents           # IBM watsonx agent wrappers
    /orchestrator     # Pipeline flow
    /integrations     # External tool stubs
    /repositories     # DB access patterns
    /utils            # Helpers
/frontend             # Placeholder (empty)
docker-compose.yml
requirements.txt
.env.example
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repo-url>
cd ORBIT
```

### 2. Environment Variables
Copy `.env.example` to `.env` and fill in your credentials.
```bash
cp .env.example .env
```

### 3. Run with Docker
```bash
docker-compose up --build
```

### 4. Local Development (Alternative)
If you want to run without Docker:
1.  Create a virtual environment: `python -m venv venv`
2.  Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
3.  Install dependencies: `pip install -r requirements.txt`
4.  Run FastAPI: `uvicorn backend.app.main:app --reload`

## API Documentation

Once the server is running, visit:
*   Swagger UI: `http://localhost:8001/docs`
*   ReDoc: `http://localhost:8001/redoc`

## Agent Pipeline

The system follows a sequential orchestration flow:
1.  **Planner**: Goal → Task list
2.  **Prioritizer**: Task list → Prioritized tasks
3.  **Scheduler**: Prioritized tasks → Assigned/Scheduled tasks
4.  **Executor**: Triggers external tools (Slack, Jira, etc.)
5.  **Insight**: Generates summary report

## IBM watsonx Integration

The system is designed to be "orchestration-ready". The agents in `backend/app/agents/` are thin wrappers that will call IBM watsonx Orchestrate skills via the `WatsonxService`.

Link of presentation: https://july-slack-72906351.figma.site/
