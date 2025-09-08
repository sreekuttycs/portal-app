from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True)
    service_group_id = Column(INTEGER(unsigned=True), ForeignKey("service_groups.id"), nullable=False)
    service_category_id = Column(INTEGER(unsigned=True), ForeignKey("service_categories.id"), nullable=False)
    specifications = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    plans = relationship("Plan", back_populates="service")