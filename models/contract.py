from sqlalchemy import Column, Integer, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    amount_due = Column(Float, nullable=False)
    created_date = Column(Date, nullable=False)
    is_signed = Column(Boolean, default=False)

    client = relationship('Client', back_populates='contracts')
    events = relationship('Event', back_populates='contract')
