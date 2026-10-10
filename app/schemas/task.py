from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from app.models.task import StatusEnum

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("Title cannot be empty or whitespace only")
            return v.strip()
        return v

class TaskStatusUpdate(BaseModel):
    status: StatusEnum

class TaskOut(TaskBase):
    id: int
    user_id: int
    status: StatusEnum
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class GenerateDescriptionRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()

class GenerateDescriptionResponse(BaseModel):
    description: str
