from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from app.database import Base


class ServiceGroup(Base):
    __tablename__ = "service_groups"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, index=True)
    slug = Column(String(50), nullable=False, unique=True, index=True)
    label = Column(String(50), nullable=False)
