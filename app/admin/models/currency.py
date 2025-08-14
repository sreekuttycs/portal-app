from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from app.database import Base

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True)
    slug = Column(String(10), unique=True, nullable=False)
    label = Column(String(100), nullable=False)
    symbol = Column(String(10), nullable=False)
