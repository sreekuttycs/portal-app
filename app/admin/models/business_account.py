from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base

class BusinessAccount(Base):
    __tablename__ = "business_accounts"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)
    slug = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    legal_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    projects = relationship("Project", back_populates="business_account")
