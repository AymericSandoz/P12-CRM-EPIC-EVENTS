from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base


class Event(Base):
    __tablename__ = 'events'

    # contract_id, client_id, event_name, event_start_date, event_end_date, support_contact, location, attendees, notes
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    event_name = Column(String(100), nullable=False)
    event_start_date = Column(Date, nullable=True)
    event_end_date = Column(Date, nullable=True)
    support_contact = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    attendees = Column(Integer, nullable=True)
    notes = Column(Text)

    client = relationship('Client', back_populates='events')
    contract = relationship('Contract', back_populates='events')

    @property
    def client_name(self):
        return self.client.full_name

    @property
    def client_contact(self):
        return f"{self.client.phone}, {self.client.email}"
