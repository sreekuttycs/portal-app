from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from app.database import Base

class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, index=True)
    slug = Column(String(50), nullable=False, unique=True, index=True)
    label = Column(String(50), nullable=False)
