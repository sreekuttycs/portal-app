from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.mysql import TINYINT, INTEGER

class Project(Base):
    __tablename__ = "projects"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, index=True)
    business_account_id = Column(INTEGER(unsigned=True), ForeignKey("business_accounts.id"), nullable=False, index=True)
    project_status_id = Column(TINYINT(unsigned=True), ForeignKey("project_statuses.id"), nullable=False, index=True)
    slug = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    short_description = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    business_account = relationship("BusinessAccount", back_populates="projects")
    project_status = relationship("ProjectStatus", back_populates="projects")
    project_members = relationship("ProjectMember", back_populates="projects")
