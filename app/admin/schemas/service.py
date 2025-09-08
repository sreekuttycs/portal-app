from typing import Optional
from pydantic import BaseModel, constr


class ServiceBase(BaseModel):
    specifications: Optional[constr(strip_whitespace=True, min_length=1)] = None
    service_group_id: int
    service_category_id: int


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    service_group_id: Optional[int] = None
    service_category_id: Optional[int] = None
    specifications: Optional[str] = None


class ServiceOut(BaseModel):
    service_id: int
    service_group: str
    service_category: str
    specifications: Optional[str]

    class Config:
        from_attributes = True 
