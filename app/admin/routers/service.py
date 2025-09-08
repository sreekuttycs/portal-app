from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.admin.models.service import Service
from app.admin.models.service_group import ServiceGroup
from app.admin.models.service_category import ServiceCategory


router = APIRouter(prefix="/services", tags=["Services"])

# ====== Schemas ======
class ServiceCreate(BaseModel):
    service_group_id: int
    service_category_id: int
    specifications: Optional[str] = None


class ServiceUpdate(BaseModel):
    service_group_id: Optional[int] = None
    service_category_id: Optional[int] = None
    specifications: Optional[str] = None


class ServiceOut(BaseModel):
    service_id: int
    service_group: str
    service_category: str
    specifications: Optional[str]

    class Config:
        orm_mode = True


# ====== List all services ======
@router.get("/", response_model=List[ServiceOut])
def get_services(db: Session = Depends(get_db)):
    services = (
        db.query(
            Service.id.label("service_id"),
            ServiceGroup.label.label("service_group"),
            ServiceCategory.label.label("service_category"),
            Service.specifications,
        )
        .join(ServiceGroup, Service.service_group_id == ServiceGroup.id)
        .join(ServiceCategory, Service.service_category_id == ServiceCategory.id)
        .all()
    )
    return services


# ====== Create service ======
@router.post("/create", response_model=int)
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    new_service = Service(
        service_group_id=data.service_group_id,
        service_category_id=data.service_category_id,
        specifications=data.specifications,
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service.id


# ====== Update service ======
@router.put("/update", response_model=int)
def update_service(service_id: int, data: ServiceUpdate, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    if data.service_group_id is not None:
        db_service.service_group_id = data.service_group_id
    if data.service_category_id is not None:
        db_service.service_category_id = data.service_category_id
    if data.specifications is not None:
        db_service.specifications = data.specifications

    db.commit()
    db.refresh(db_service)
    return db_service.id


# ====== Service details ======
@router.get("/details", response_model=ServiceOut)
def service_details(service_id: int = Query(...), db: Session = Depends(get_db)):
    db_service = (
        db.query(
            Service.id.label("service_id"),
            ServiceGroup.label.label("service_group"),
            ServiceCategory.label.label("service_category"),
            Service.specifications,
        )
        .join(ServiceGroup, Service.service_group_id == ServiceGroup.id)
        .join(ServiceCategory, Service.service_category_id == ServiceCategory.id)
        .filter(Service.id == service_id)
        .first()
    )
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service


# ====== Delete service ======
@router.delete("/delete", response_model=bool)
def delete_service(service_id: int = Query(...), db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(db_service)
    db.commit()
    return True
