from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ProjectMemberBase(BaseModel):
    project_id: int
    member_role_id: int
    member_id: int

     # Extra fields from Member table (for listing purpose)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class ProjectMemberCreate(ProjectMemberBase):
    pass


class ProjectMemberUpdate(ProjectMemberBase):
    pass


class ProjectMemberOut(ProjectMemberBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
