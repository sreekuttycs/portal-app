from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional
from enum import IntEnum


class PaymentMode(IntEnum):
    ONLINE = 1
    OFFLINE = 2


class SubscriptionCreate(BaseModel):
    plan_id: int
    payment_mode_id: PaymentMode
    member_id: int
    amount: Decimal
    start_date: date
    locking_period: str
    bill_due_date: Optional[date] = None
    term_days: int | None = None


class SubscriptionOut(BaseModel):
    id: int
    plan_id: int
    payment_mode_id: PaymentMode
    member_id: int
    amount: Decimal
    start_date: date
    locking_period: str
    bill_due_date: Optional[date]
    is_paid: bool
    status: int

    class Config:
        orm_mode = True
