from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    dob: Optional[datetime] = None
    gender: Optional[str] = None
    mobile: str
    password: str

class UserCreate(UserBase):
    pass

class Login(BaseModel):
    mobile: str
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
