from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database import Base

class ProjectStatus(Base):
    __tablename__ = "project_statuses"

    id = Column(TINYINT(unsigned=True), primary_key=True, autoincrement=True)
    slug = Column(String(50), nullable=False, unique=True, index=True)
    label = Column(String(50), nullable=False)

    projects = relationship("Project", back_populates="project_status")
