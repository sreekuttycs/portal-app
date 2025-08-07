from sqlalchemy import Column, Integer, String
from app.database import Base

class MemberRole(Base):
    __tablename__ = "member_roles"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(50), unique=True, nullable=False)
    label = Column(String(100), nullable=False)
