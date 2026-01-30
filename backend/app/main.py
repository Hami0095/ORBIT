from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import auth, goals, tasks, team, orchestrate
from backend.app.core.config import settings
from backend.app.utils.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(goals.router, prefix=f"{settings.API_V1_STR}/goals", tags=["goals"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"])
app.include_router(team.router, prefix=f"{settings.API_V1_STR}/team", tags=["team"])
app.include_router(orchestrate.router, prefix=f"{settings.API_V1_STR}/orchestrate", tags=["orchestrate"])

@app.get("/")
async def root():
    return {"message": "Welcome to ORBIT - AI Task Orchestrator API"}
