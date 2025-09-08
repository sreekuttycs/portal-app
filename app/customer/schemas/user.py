from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    mobile_number: Optional[str] = None
    email: str
    password: str  # plaintext; should be hashed before storing

class UserResponse(BaseModel):
    id: int
    username: str
    mobile_number: Optional[str] = None
    email: str
    email_verified_at: Optional[datetime]
    remember_token: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
