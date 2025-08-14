from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MemberAddressBase(BaseModel):
    member_id: int
    country_id: int
    first_name: str
    last_name: Optional[str] = None
    phone: str
    email: Optional[str] = None
    address_line_1: str
    address_line_2: str
    city: str
    postal_code: str

class MemberAddressCreate(MemberAddressBase):
    pass

class MemberAddressUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None

class MemberAddressOut(MemberAddressBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
