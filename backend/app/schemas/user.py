from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
import re
from backend.app.db.models import UserRole

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.MANAGER

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        # Strict regex for business-like emails
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, v):
            raise ValueError("Invalid email format. Please provide a valid email.")
        return v

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass
