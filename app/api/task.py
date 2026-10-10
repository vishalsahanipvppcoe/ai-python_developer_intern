from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate, TaskOut, GenerateDescriptionRequest, GenerateDescriptionResponse
from app.services.task import create_task, get_user_tasks, get_task, update_task, update_task_status
from app.auth.dependencies import get_current_user, get_current_admin_user
from app.models.user import User
from app.ai.gemini import generate_task_description

router = APIRouter()

@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task for the logged-in user."""
    return create_task(db, task_in, current_user)

@router.post("/generate-description", response_model=GenerateDescriptionResponse)
def generate_description(
    request: GenerateDescriptionRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate a task description using AI."""
    description = generate_task_description(request.title)
    return {"description": description}

@router.get("", response_model=List[TaskOut])
def read_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List tasks (all tasks if admin, otherwise only user's tasks)."""
    return get_user_tasks(db, current_user)

@router.get("/{task_id}", response_model=TaskOut)
def read_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task."""
    return get_task(db, task_id, current_user)

@router.patch("/{task_id}", response_model=TaskOut)
def patch_task(
    task_id: int,
    task_in: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update title and description of a task."""
    return update_task(db, task_id, task_in, current_user)

@router.patch("/{task_id}/status", response_model=TaskOut)
def patch_task_status(
    task_id: int,
    status_in: TaskStatusUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update status of a task (Admin only)."""
    return update_task_status(db, task_id, status_in, current_user)
