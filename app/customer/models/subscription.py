from sqlalchemy import Column, String, ForeignKey, Date, DateTime, Numeric, Boolean, SmallInteger, func
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from enum import IntEnum
from app.database import Base


class PaymentMode(IntEnum):
    ONLINE = 1
    OFFLINE = 2


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)
    plan_id = Column(INTEGER(unsigned=True), ForeignKey("plans.id"), nullable=False, index=True)
    payment_mode_id = Column(
        TINYINT(unsigned=True),
        nullable=False,
        index=True,
        comment="1 = Online, 2 = Offline"
    )
    member_id = Column(INTEGER(unsigned=True), ForeignKey("members.id"), nullable=False)

    amount = Column(Numeric(9, 2), nullable=False)
    start_date = Column(Date, nullable=False)
    locking_period = Column(String(255), nullable=False)
    bill_due_date = Column(Date, nullable=True)

    is_paid = Column(Boolean, nullable=False, server_default=text("0"))
    status = Column(TINYINT(unsigned=True), nullable=False, server_default=text("1"))

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    plan = relationship("Plan", back_populates="subscriptions")
    member = relationship("Member", back_populates="subscriptions")
