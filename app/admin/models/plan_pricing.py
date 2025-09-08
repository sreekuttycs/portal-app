from sqlalchemy import Column, String, ForeignKey, DateTime, Numeric, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base


class PlanPricing(Base):
    __tablename__ = "plan_pricing"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True)
    plan_id = Column(INTEGER(unsigned=True), ForeignKey("plans.id"), nullable=False)
    currency_id = Column(INTEGER(unsigned=True), ForeignKey("currencies.id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)  # 10 digits, 2 decimal places

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    plan = relationship("Plan", back_populates="pricings")
    currency = relationship("Currency", back_populates="pricings")
