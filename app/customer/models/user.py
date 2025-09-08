from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    mobile_number = Column(String(15), unique=True, nullable=True)
    email = Column(String(255), nullable=False, index=True)
    email_verified_at = Column(TIMESTAMP, nullable=True)
    password = Column(String(255), nullable=False)
    remember_token = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)

    members = relationship("Member", back_populates="user")
    email_verifications = relationship("UserEmailVerification", back_populates="user")

