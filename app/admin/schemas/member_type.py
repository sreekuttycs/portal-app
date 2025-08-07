from pydantic import BaseModel, constr

# Shared properties
class MemberTypeBase(BaseModel):
    slug: constr(strip_whitespace=True, min_length=1)
    label: constr(strip_whitespace=True, min_length=1)

# For creating a new member type
class MemberTypeCreate(MemberTypeBase):
    pass

# For updating an existing member type
class MemberTypeUpdate(BaseModel):
    slug: str | None = None
    label: str | None = None

# For returning member type from DB
class MemberTypeOut(MemberTypeBase):
    id: int

    class Config:
        orm_mode = True
