from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MemberBankAccountBase(BaseModel):
    member_id: int
    bank_holder_name: str
    branch: str
    ifsc_code: Optional[str] = None
    swift_code: Optional[str] = None
    account_number: str


class MemberBankAccountCreate(MemberBankAccountBase):
    pass


class MemberBankAccountUpdate(BaseModel):
    bank_holder_name: Optional[str] = None
    branch: Optional[str] = None
    ifsc_code: Optional[str] = None
    swift_code: Optional[str] = None
    account_number: Optional[str] = None


class MemberBankAccountOut(MemberBankAccountBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
