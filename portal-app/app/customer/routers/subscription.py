from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from app.database import get_db
from app.admin.models.plan import Plan
from app.admin.models.plan_pricing import PlanPricing
from app.customer.models.subscription import Subscription
from app.admin.models.currency import Currency
from app.admin.models.member import Member
from app.customer.schemas.subscription import SubscriptionCreate, SubscriptionOut

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

# ========= Get All Plans =========
@router.get("/plans")
def get_plans(db: Session = Depends(get_db)):
    plans = (
        db.query(
            Plan.id.label("plan_id"),
            Plan.service_id,
            Plan.slug.label("plan_slug"),
            Plan.label.label("plan_label"),
            # assuming service relationships
            # Plan.service_group_name, Plan.service_category_name,
            PlanPricing.amount,
            Currency.label.label("currency_name"),
            Currency.symbol.label("currency_symbol"),
        )
        .join(PlanPricing, PlanPricing.plan_id == Plan.id)
        .join(Currency, PlanPricing.currency_id == Currency.id)
        .all()
    )

    output = []
    for plan in plans:
        output.append({
            "plan_id": plan.plan_id,
            "service_id": plan.service_id,
            "plan_slug": plan.plan_slug,
            "plan_label": plan.plan_label,
            # "service_group_name": plan.service_group_name,
            # "service_category_name": plan.service_category_name,
            "currency_name": plan.currency_name,
            "currency_symbol": plan.currency_symbol,
            "amount": str(plan.amount),
        })

    return output


# ========= Create Subscription =========
@router.post("/create", response_model=SubscriptionOut)
def create_subscription(data: SubscriptionCreate, db: Session = Depends(get_db)):
    # 1. Validate plan pricing
    plan_pricing = db.query(PlanPricing).filter(PlanPricing.plan_id == data.plan_id).first()
    if not plan_pricing:
        raise HTTPException(status_code=404, detail="Plan not found")

    # 2. Create subscription
    subscription = Subscription(
        plan_id=data.plan_id,
        payment_mode_id=data.payment_mode_id.value,  # enum
        member_id=data.member_id,
        amount=plan_pricing.amount,
        start_date=data.start_date,
        locking_period=data.locking_period,
        bill_due_date=data.bill_due_date,
        is_paid=False,
        status=1,
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    # 3. Compute due date (using term days)
    term_days = data.term_days or 30
    due_date = subscription.start_date + timedelta(days=term_days)

    # (Optional) Create invoice + items in separate table

    return subscription
