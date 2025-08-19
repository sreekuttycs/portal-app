from pydantic import BaseModel


class ServiceGroupBase(BaseModel):
    slug: str
    label: str


class ServiceGroupCreate(ServiceGroupBase):
    pass


class ServiceGroupUpdate(ServiceGroupBase):
    pass


class ServiceGroupResponse(ServiceGroupBase):
    id: int   # <-- INT type from DB

    class Config:
        orm_mode = True
