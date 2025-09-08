from pydantic import BaseModel, constr
from typing import Optional


# ===== Base =====
class PlanBase(BaseModel):
    slug: constr(strip_whitespace=True, min_length=1)
    label: constr(strip_whitespace=True, min_length=1)


# ===== Create =====
class PlanCreate(PlanBase):
    service_id: int   # must belong to a Service


# ===== Update =====
class PlanUpdate(BaseModel):
    slug: Optional[str] = None
    label: Optional[str] = None
    service_id: Optional[int] = None


# ===== Output =====
class PlanOut(PlanBase):
    id: int
    service_id: int

    class Config:
        orm_mode = True
