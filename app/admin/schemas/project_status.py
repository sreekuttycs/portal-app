from pydantic import BaseModel

class ProjectStatusBase(BaseModel):
    slug: str
    label: str

class ProjectStatusCreate(ProjectStatusBase):
    pass

class ProjectStatusUpdate(ProjectStatusBase):
    pass

class ProjectStatusOut(ProjectStatusBase):
    id: int

    class Config:
        orm_mode = True
