from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.sql import func


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(12), nullable=False)
    company_name = Column(String(255), nullable=False)
    created_date = Column(Date, nullable=False, default=func.now())
    last_contact_date = Column(Date, required=False)
    contact_person = Column(String(255), nullable=False)

    contracts = relationship('Contract', back_populates='client')
    events = relationship('Event', back_populates='client')
