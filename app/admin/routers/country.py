from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.admin.models.country import Country
from app.admin.schemas.country import (
    CountryCreate, CountryUpdate, CountryOut, CountryIDRequest
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create
@router.post("/", response_model=CountryOut)
def create_country(data: CountryCreate, db: Session = Depends(get_db)):
    if db.query(Country).filter(Country.code == data.code).first():
        raise HTTPException(status_code=400, detail="Country code already exists")
    country = Country(**data.dict())
    db.add(country)
    db.commit()
    db.refresh(country)
    return country


# List all
@router.get("/list", response_model=List[CountryOut])
def list_countries(db: Session = Depends(get_db)):
    return db.query(Country).all()


# Get detail (via body)
@router.post("/detail", response_model=CountryOut)
def get_country(request: CountryIDRequest, db: Session = Depends(get_db)):
    country = db.get(Country, request.country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


# Update (via body)
@router.put("/update", response_model=CountryOut)
def update_country(data: CountryUpdate, request: CountryIDRequest, db: Session = Depends(get_db)):
    country = db.get(Country, request.country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # Duplicate code check
    if data.code and data.code != country.code:
        if db.query(Country).filter(Country.code == data.code).first():
            raise HTTPException(status_code=400, detail="Country code already exists")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(country, key, value)

    db.commit()
    db.refresh(country)
    return country


# Delete (via body)
@router.delete("/delete", status_code=204)
def delete_country(request: CountryIDRequest, db: Session = Depends(get_db)):
    country = db.get(Country, request.country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    db.delete(country)
    db.commit()
    return
