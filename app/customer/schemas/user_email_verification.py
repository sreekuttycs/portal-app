from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserEmailVerificationBase(BaseModel):
    user_id: int
    email_address: EmailStr
    verification_token: str


class UserEmailVerificationCreate(UserEmailVerificationBase):
    pass


class UserEmailVerificationUpdate(BaseModel):
    verified_at: Optional[datetime] = None


class UserEmailVerificationOut(UserEmailVerificationBase):
    id: int
    verified_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
