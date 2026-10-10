from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
