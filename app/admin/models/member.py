from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey("users.id"), nullable=False)
    member_type_id = Column(INTEGER(unsigned=True), ForeignKey("member_types.id"), nullable=False)

    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="members")
    member_type = relationship("MemberType", back_populates="members")
    addresses = relationship("MemberAddress", back_populates="member")
    bank_accounts = relationship("MemberBankAccount", back_populates="member")


