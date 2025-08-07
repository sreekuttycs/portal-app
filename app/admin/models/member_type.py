from sqlalchemy import Column, Integer, String
from app.database import Base

class MemberType(Base):
    __tablename__ = "member_types"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(50), unique=True, nullable=False)
    label = Column(String(100), nullable=False)