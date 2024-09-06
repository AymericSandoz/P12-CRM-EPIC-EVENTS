from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base


class Event(Base):
    __tablename__ = 'events'

    # contract_id, client_id, event_name, event_start_date, event_end_date, support_contact, location, attendees, notes
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    event_name = Column(String(255), nullable=False)
    event_start_date = Column(Date, nullable=False)
    event_end_date = Column(Date, nullable=False)
    support_contact = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(Text)

    client = relationship('Client', back_populates='events')
    contract = relationship('Contract', back_populates='events')
