from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.database import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False, unique=True)

    member_addresses = relationship("MemberAddress", back_populates="country")

