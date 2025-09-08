from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BusinessAccountBase(BaseModel):
    slug: str
    name: str
    legal_name: str


class BusinessAccountCreate(BusinessAccountBase):
    pass


class BusinessAccountUpdate(BusinessAccountBase):
    id: int   # update needs id


class BusinessAccountOut(BusinessAccountBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class BusinessAccountIdRequest(BaseModel):
    id: int