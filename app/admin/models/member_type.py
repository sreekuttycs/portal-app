from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base

class MemberType(Base):
    __tablename__ = "member_types"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True)
    slug = Column(String(50), unique=True, nullable=False)
    label = Column(String(100), nullable=False)

    members = relationship("Member", back_populates="member_type")
