from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
