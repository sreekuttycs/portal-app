from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base

class MemberAddress(Base):
    __tablename__ = "member_addresses"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    member_id = Column(INTEGER(unsigned=True), ForeignKey("members.id"), nullable=False)
    country_id = Column(INTEGER(unsigned=True), ForeignKey("countries.id"), nullable=False)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)
    phone = Column(String(25), nullable=False)
    email = Column(String(255), nullable=True)
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    postal_code = Column(String(25), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    member = relationship("Member", back_populates="addresses")
    country = relationship("Country", back_populates="member_addresses")
