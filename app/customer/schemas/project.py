from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ProjectBase(BaseModel):
    business_account_id: int
    project_status_id: int
    slug: str
    name: str
    short_description: str
    start_date: date
    business_account_name: Optional[str]
    updated_at: datetime

class ProjectStatusOut(BaseModel):
    id: int
    label: str

class ProjectSlugRequest(BaseModel):
    slug: str

class ProjectIDRequest(BaseModel):
    project_id: int

class ProjectMemberOut(BaseModel):
    id: int
    project_id: int
    member_id: int   
    first_name: Optional[str] = None   # from Member
    last_name: Optional[str] = None    # from Member
    member_role: Optional[str] = None
    phone: Optional[str] = None 
    email: Optional[str] = None  
  
    
class ProjectOut(ProjectBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
