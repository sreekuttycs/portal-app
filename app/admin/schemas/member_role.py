from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MemberRoleBase(BaseModel):
    slug: str
    label: str


class MemberRoleCreate(MemberRoleBase):
    pass


class MemberRoleUpdate(MemberRoleBase):
    id: int   # required for update


class MemberRoleOut(MemberRoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class MemberRoleIdRequest(BaseModel):
    id: int
