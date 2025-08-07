from pydantic import BaseModel, constr

# Shared fields
class MemberRoleBase(BaseModel):
    slug: constr(strip_whitespace=True, min_length=1)
    label: constr(strip_whitespace=True, min_length=1)

# For creating
class MemberRoleCreate(MemberRoleBase):
    pass

# For updating
class MemberRoleUpdate(BaseModel):
    slug: str | None = None
    label: str | None = None

# For returning to client
class MemberRoleOut(MemberRoleBase):
    id: int

    class Config:
        orm_mode = True
