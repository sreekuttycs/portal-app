from sqlalchemy import Column, Integer, String
from app.database import Base

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(10), unique=True, nullable=False)
    label = Column(String(100), nullable=False)
    symbol = Column(String(10), nullable=False)
