from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.admin.models.plan import Plan
from app.admin.models.service import Service
from app.admin.models.plan_pricing import PlanPricing
from pydantic import BaseModel

router = APIRouter(prefix="/plans", tags=["Plans"])


# ====== Schemas ======
class PlanCreate(BaseModel):
    service_id: int
    slug: str
    label: str


class PlanUpdate(BaseModel):
    service_id: Optional[int] = None
    slug: Optional[str] = None
    label: Optional[str] = None


class PlanOut(BaseModel):
    plan_id: int
    service_id: int
    service_name: Optional[str]
    slug: str
    label: str

    class Config:
        orm_mode = True


# ====== List all plans ======
@router.get("/", response_model=List[PlanOut])
def get_plans(db: Session = Depends(get_db)):
    plans = (
        db.query(
            Plan.id.label("plan_id"),
            Plan.service_id,
            Service.specifications.label("service_name"),  # or group/category if needed
            Plan.slug,
            Plan.label,
        )
        .join(Service, Plan.service_id == Service.id)
        .all()
    )
    return plans


# ====== Create plan ======
@router.post("/create", response_model=int)
def create_plan(data: PlanCreate, db: Session = Depends(get_db)):
    new_plan = Plan(
        service_id=data.service_id,
        slug=data.slug,
        label=data.label,
    )
    db.add(new_plan)
    db.flush()  # get ID before commit
    plan_id = new_plan.id
    db.commit()
    db.refresh(new_plan)
    return plan_id


# ====== Update plan ======
@router.put("/update", response_model=int)
def update_plan(plan_id: int, data: PlanUpdate, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    if data.service_id is not None:
        plan.service_id = data.service_id
    if data.slug is not None:
        plan.slug = data.slug
    if data.label is not None:
        plan.label = data.label

    db.commit()
    db.refresh(plan)
    return plan.id


# ====== Plan details ======
@router.get("/details", response_model=Optional[PlanOut])
def plan_details(plan_id: int = Query(...), db: Session = Depends(get_db)):
    plan = (
        db.query(
            Plan.id.label("plan_id"),
            Plan.service_id,
            Service.specifications.label("service_name"),
            Plan.slug,
            Plan.label,
        )
        .join(Service, Plan.service_id == Service.id)
        .filter(Plan.id == plan_id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


# ====== Delete plan ======
@router.delete("/delete", response_model=bool)
def delete_plan(plan_id: int = Query(...), db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    db.query(PlanPricing).filter(PlanPricing.plan_id == plan_id).delete(synchronize_session=False)
    db.delete(plan)
    db.commit()
    return True
