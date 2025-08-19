from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.admin.models.service_category import ServiceCategory
from app.admin.schemas.service_category import (
    ServiceCategoryCreate,
    ServiceCategoryUpdate,
    ServiceCategoryOut,
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ServiceCategoryOut)
def create_service_category(data: ServiceCategoryCreate, db: Session = Depends(get_db)):
    db_obj = ServiceCategory(**data.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/", response_model=List[ServiceCategoryOut])
def list_service_categories(db: Session = Depends(get_db)):
    return db.query(ServiceCategory).all()


@router.get("/{category_id}", response_model=ServiceCategoryOut)
def get_service_category(category_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Service Category not found")
    return db_obj


@router.put("/{category_id}", response_model=ServiceCategoryOut)
def update_service_category(category_id: int, data: ServiceCategoryUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Service Category not found")
    for key, value in data.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.delete("/{category_id}")
def delete_service_category(category_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Service Category not found")
    db.delete(db_obj)
    db.commit()
    return {"message": "Service Category deleted successfully"}
