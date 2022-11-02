from .db import Base, SessionLocal, get_db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    lat = Column(String, nullable=False)
    lng = Column(String, nullable=False)
