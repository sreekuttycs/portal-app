from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MemberTypeBase(BaseModel):
    slug: str
    label: str


class MemberTypeCreate(MemberTypeBase):
    pass


class MemberTypeUpdate(MemberTypeBase):
    id: int   # required for update


class MemberTypeOut(MemberTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# for details/delete
class MemberTypeIdRequest(BaseModel):
    id: int
