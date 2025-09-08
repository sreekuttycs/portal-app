from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.admin.models.currency import Currency
from app.admin.schemas.currency import (
    CurrencyCreate, CurrencyUpdate, CurrencyOut, CurrencyIDRequest
)

router = APIRouter()

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


# List all
@router.get("/list", response_model=List[CurrencyOut])
def list_currencies(db: Session = Depends(get_db)):
    return db.query(Currency).all()


# Get detail (via body)
@router.post("/detail", response_model=CurrencyOut)
def get_currency(request: CurrencyIDRequest, db: Session = Depends(get_db)):
    currency = db.get(Currency, request.currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency


# Update (via body)
@router.put("/update", response_model=CurrencyOut)
def update_currency(data: CurrencyUpdate, request: CurrencyIDRequest, db: Session = Depends(get_db)):
    currency = db.get(Currency, request.currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")

    # optional: duplicate slug check
    if data.slug and data.slug != currency.slug:
        if db.query(Currency).filter(Currency.slug == data.slug).first():
            raise HTTPException(status_code=400, detail="Slug already exists")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(currency, key, value)

    db.commit()
    db.refresh(currency)
    return currency


# Delete (via body)
@router.delete("/delete", status_code=204)
def delete_currency(request: CurrencyIDRequest, db: Session = Depends(get_db)):
    currency = db.get(Currency, request.currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    db.delete(currency)
    db.commit()
    return
