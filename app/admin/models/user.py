from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import BIGINT
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True, autoincrement=True)
    short_name = Column(String(5), nullable=False)
    display_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    email_verified_at = Column(TIMESTAMP, nullable=True)
    password = Column(String(255), nullable=False)
    remember_token = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)
