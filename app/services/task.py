from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task import Task
from app.models.user import User, RoleEnum
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate

def create_task(db: Session, task_in: TaskCreate, user: User) -> Task:
    db_task = Task(
        title=task_in.title,
        description=task_in.description,
        user_id=user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_user_tasks(db: Session, user: User):
    if user.role == RoleEnum.admin:
        return db.query(Task).all()
    return db.query(Task).filter(Task.user_id == user.id).all()

def get_task(db: Session, task_id: int, user: User) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.user_id != user.id and user.role != RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return task

def update_task(db: Session, task_id: int, task_in: TaskUpdate, user: User) -> Task:
    task = get_task(db, task_id, user)
    
    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
        
    db.commit()
    db.refresh(task)
    return task

def update_task_status(db: Session, task_id: int, status_in: TaskStatusUpdate, admin_user: User) -> Task:
    if admin_user.role != RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    task.status = status_in.status
    db.commit()
    db.refresh(task)
    return task
