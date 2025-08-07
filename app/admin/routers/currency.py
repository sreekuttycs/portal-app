from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.admin.models.currency import Currency
from app.admin.schemas.currency import CurrencyCreate, CurrencyUpdate, CurrencyOut

router = APIRouter(
    prefix="/admin/currencies",
    tags=["Currencies"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create currency
@router.post("/", response_model=CurrencyOut)
def create_currency(data: CurrencyCreate, db: Session = Depends(get_db)):
    if db.query(Currency).filter(Currency.slug == data.slug).first():
        raise HTTPException(status_code=400, detail="Slug already exists")
    currency = Currency(**data.dict())
    db.add(currency)
    db.commit()
    db.refresh(currency)
    return currency

# Get all currencies
@router.get("/", response_model=list[CurrencyOut])
def list_currencies(db: Session = Depends(get_db)):
    return db.query(Currency).all()

# Get single currency
@router.get("/{currency_id}", response_model=CurrencyOut)
def get_currency(currency_id: int, db: Session = Depends(get_db)):
    currency = db.query(Currency).get(currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency

# Update currency
@router.put("/{currency_id}", response_model=CurrencyOut)
def update_currency(currency_id: int, data: CurrencyUpdate, db: Session = Depends(get_db)):
    currency = db.query(Currency).get(currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(currency, key, value)

    db.commit()
    db.refresh(currency)
    return currency

# Delete currency
@router.delete("/{currency_id}", status_code=204)
def delete_currency(currency_id: int, db: Session = Depends(get_db)):
    currency = db.query(Currency).get(currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    db.delete(currency)
    db.commit()
    return
