from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True)
    service_id = Column(INTEGER(unsigned=True), ForeignKey("services.id"), nullable=False)

    slug = Column(String(255), nullable=False, unique=True)
    label = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    service = relationship("Service", back_populates="plans")
    pricings = relationship("PlanPricing", back_populates="plan", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="plan")
