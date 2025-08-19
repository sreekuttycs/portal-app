from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.admin.models.service_group import ServiceGroup
from app.admin.schemas.service_group import (
    ServiceGroupCreate,
    ServiceGroupUpdate,
    ServiceGroupResponse,
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ServiceGroupResponse)
def create_service_group(data: ServiceGroupCreate, db: Session = Depends(get_db)):
    new_group = ServiceGroup(**data.dict())
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


@router.get("/", response_model=List[ServiceGroupResponse])
def list_service_groups(db: Session = Depends(get_db)):
    return db.query(ServiceGroup).all()


@router.get("/{group_id}", response_model=ServiceGroupResponse)
def get_service_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(ServiceGroup).filter(ServiceGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Service group not found")
    return group


@router.put("/{group_id}", response_model=ServiceGroupResponse)
def update_service_group(group_id: int, data: ServiceGroupUpdate, db: Session = Depends(get_db)):
    group = db.query(ServiceGroup).filter(ServiceGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Service group not found")
    for field, value in data.dict().items():
        setattr(group, field, value)
    db.commit()
    db.refresh(group)
    return group


@router.delete("/{group_id}")
def delete_service_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(ServiceGroup).filter(ServiceGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Service group not found")
    db.delete(group)
    db.commit()
    return {"detail": "Service group deleted"}
