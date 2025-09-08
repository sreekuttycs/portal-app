from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator
from decimal import Decimal
from typing import List, Optional
from app.database import get_db
from app.admin.models.plan_pricing import PlanPricing
from app.admin.models.plan import Plan
from app.admin.models.currency import Currency

router = APIRouter(prefix="/plan-pricing", tags=["Plan Pricing"])

# ====== Schemas ======
class PlanPricingCreate(BaseModel):
    plan_id: int
    currency_id: int
    amount: Decimal

    @validator("amount")
    def validate_amount(cls, v):
        if v >= 10**10:
            raise ValueError("Amount exceeds max digits (10)")
        return round(v, 2)


class PlanPricingUpdate(BaseModel):
    currency_id: Optional[int] = None
    amount: Optional[Decimal] = None

    @validator("amount")
    def validate_amount(cls, v):
        if v is not None and v >= 10**10:
            raise ValueError("Amount exceeds max digits (10)")
        return round(v, 2) if v is not None else v


class PlanPricingOut(BaseModel):
    id: int
    plan_id: int
    currency_id: int
    amount: Decimal
    plan_label: Optional[str]
    currency_code: Optional[str]

    class Config:
        orm_mode = True


# ====== List all plan pricing ======
@router.get("/", response_model=List[PlanPricingOut])
def get_plan_pricing(db: Session = Depends(get_db)):
    pricing = (
        db.query(
            PlanPricing.id,
            PlanPricing.plan_id,
            PlanPricing.currency_id,
            PlanPricing.amount,
            Plan.label.label("plan_label"),
            Currency.slug.label("currency_code"),
        )
        .join(Plan, PlanPricing.plan_id == Plan.id)
        .join(Currency, PlanPricing.currency_id == Currency.id)
        .all()
    )
    return pricing


# ====== Create plan pricing ======
@router.post("/create", response_model=int)
def create_plan_pricing(data: PlanPricingCreate, db: Session = Depends(get_db)):
    new_pricing = PlanPricing(**data.dict())
    db.add(new_pricing)
    db.flush()  # get ID before commit
    pricing_id = new_pricing.id
    db.commit()
    db.refresh(new_pricing)
    return pricing_id


# ====== Update plan pricing ======
@router.put("/update", response_model=int)
def update_plan_pricing(pricing_id: int, data: PlanPricingUpdate, db: Session = Depends(get_db)):
    pricing = db.query(PlanPricing).filter(PlanPricing.id == pricing_id).first()
    if not pricing:
        raise HTTPException(status_code=404, detail="Plan pricing not found")

    if data.currency_id is not None:
        pricing.currency_id = data.currency_id
    if data.amount is not None:
        pricing.amount = data.amount

    db.commit()
    db.refresh(pricing)
    return pricing.id


# ====== Plan pricing details ======
@router.get("/details", response_model=Optional[PlanPricingOut])
def plan_pricing_details(pricing_id: int = Query(...), db: Session = Depends(get_db)):
    pricing = (
        db.query(
            PlanPricing.id,
            PlanPricing.plan_id,
            PlanPricing.currency_id,
            PlanPricing.amount,
            Plan.label.label("plan_label"),
            Currency.slug.label("currency_code"),
        )
        .join(Plan, PlanPricing.plan_id == Plan.id)
        .join(Currency, PlanPricing.currency_id == Currency.id)
        .filter(PlanPricing.id == pricing_id)
        .first()
    )
    if not pricing:
        raise HTTPException(status_code=404, detail="Plan pricing not found")
    return pricing


# ====== Delete plan pricing ======
@router.delete("/delete", response_model=bool)
def delete_plan_pricing(pricing_id: int = Query(...), db: Session = Depends(get_db)):
    pricing = db.query(PlanPricing).filter(PlanPricing.id == pricing_id).first()
    if not pricing:
        raise HTTPException(status_code=404, detail="Plan pricing not found")

    db.delete(pricing)
    db.commit()
    return True
