from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from app.database import Base
from sqlalchemy.orm import relationship


class MemberRole(Base):
    __tablename__ = "member_roles"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True)
    slug = Column(String(50), unique=True, nullable=False)
    label = Column(String(100), nullable=False)

    project_members = relationship("ProjectMember", back_populates="member_role")
