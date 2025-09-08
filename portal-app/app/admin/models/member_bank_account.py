from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base


class MemberBankAccount(Base):
    __tablename__ = "member_bank_accounts"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)
    member_id = Column(INTEGER(unsigned=True), ForeignKey("members.id"), nullable=False, index=True)
    bank_holder_name = Column(String(255), nullable=False)
    branch = Column(String(255), nullable=False)
    ifsc_code = Column(String(50), nullable=True)
    swift_code = Column(String(50), nullable=True)
    account_number = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)

    # relationship (if you want to link with Member model)
    member = relationship("Member", back_populates="bank_accounts")
