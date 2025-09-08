from pydantic import BaseModel, constr

class CurrencyBase(BaseModel):
    slug: constr(strip_whitespace=True, min_length=1)
    label: constr(strip_whitespace=True, min_length=1)
    symbol: constr(strip_whitespace=True, min_length=1)

class CurrencyCreate(CurrencyBase):
    pass

class CurrencyUpdate(BaseModel):
    slug: str | None = None
    label: str | None = None
    symbol: str | None = None

class CurrencyOut(CurrencyBase):
    id: int

class CurrencyIDRequest(BaseModel):
    currency_id: int    

    class Config:
        orm_mode = True
