from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    project_id = Column(INTEGER(unsigned=True), ForeignKey("projects.id"), nullable=False, index=True)
    member_role_id = Column(INTEGER(unsigned=True), ForeignKey("member_roles.id"), nullable=False, index=True)
    member_id = Column(INTEGER(unsigned=True), ForeignKey("members.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    projects = relationship("Project", back_populates="project_members")
    member_role = relationship("MemberRole", back_populates="project_members")
    member = relationship("Member", back_populates="project_members")
