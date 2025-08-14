from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class MemberBase(BaseModel):
    user_id: int
    member_type_id: int
    first_name: str
    last_name: str
    phone: Optional[str]
    email: EmailStr

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None    

class MemberOut(MemberBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True