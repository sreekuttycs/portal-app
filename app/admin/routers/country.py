from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.admin.models.country import Country
from app.admin.schemas.country import CountryCreate, CountryUpdate, CountryOut

router = APIRouter(
    prefix="/admin/countries",
    tags=["Countries"]
)

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
@router.get("/", response_model=list[CountryOut])
def list_countries(db: Session = Depends(get_db)):
    return db.query(Country).all()

# Get one
@router.get("/{country_id}", response_model=CountryOut)
def get_country(country_id: int, db: Session = Depends(get_db)):
    country = db.query(Country).get(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

# Update
@router.put("/{country_id}", response_model=CountryOut)
def update_country(country_id: int, data: CountryUpdate, db: Session = Depends(get_db)):
    country = db.query(Country).get(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(country, key, value)
    db.commit()
    db.refresh(country)
    return country

# Delete
@router.delete("/{country_id}", status_code=204)
def delete_country(country_id: int, db: Session = Depends(get_db)):
    country = db.query(Country).get(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    db.delete(country)
    db.commit()
    return
