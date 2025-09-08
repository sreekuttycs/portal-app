from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base

class UserEmailVerification(Base):
    __tablename__ = "user_email_verifications"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey("users.id"), nullable=False, index=True)
    email_address = Column(String(255), nullable=False)
    verification_token = Column(String(255), nullable=False)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="email_verifications")
