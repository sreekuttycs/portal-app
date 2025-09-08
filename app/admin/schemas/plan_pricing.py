from sqlalchemy import Column, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class PlanPricing(Base):
    __tablename__ = "plan_pricing"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)
    plan_id = Column(INTEGER(unsigned=True), ForeignKey("plans.id", ondelete="CASCADE"), nullable=False)
    currency_id = Column(INTEGER(unsigned=True), ForeignKey("currencies.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    plan = relationship("Plan", back_populates="pricing")
    currency = relationship("Currency", back_populates="pricing")
