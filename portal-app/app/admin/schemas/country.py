from pydantic import BaseModel, constr

class CountryBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    code: constr(strip_whitespace=True, min_length=1, max_length=5)

class CountryCreate(CountryBase):
    pass

class CountryUpdate(BaseModel):
    name: str | None = None
    code: str | None = None

class CountryOut(CountryBase):
    id: int

    class Config:
        orm_mode = True
