from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.task import router as task_router

app = FastAPI(title="AI-Powered Task Management System")

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(task_router, prefix="/api/tasks", tags=["tasks"])

@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok", "message": "API is running!"}
