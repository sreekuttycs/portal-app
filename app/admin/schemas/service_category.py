from pydantic import BaseModel

class ServiceCategoryBase(BaseModel):
    slug: str
    label: str

class ServiceCategoryCreate(ServiceCategoryBase):
    pass

class ServiceCategoryUpdate(ServiceCategoryBase):
    pass

class ServiceCategoryOut(ServiceCategoryBase):
    id: int

    class Config:
        from_attributes = True   # important for ORM -> Pydantic
