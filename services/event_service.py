from models import Event, Session


class Event_services():
    def create(name, date, contract_id, client_id, support_contact, location, attendees, notes):
        session = Session()
        event = Event(
            event_name=name,
            event_start_date=date,
            event_end_date=date,
            contract_id=contract_id,
            client_id=client_id,
            support_contact=support_contact,
            location=location,
            attendees=attendees,
            notes=notes
        )
        session.add(event)
        session.commit()
        session.close()

    def get_all():
        session = Session()
        events = session.query(Event).all()
        session.close()
        return events

    def get(event_id):
        session = Session()
        event = session.query(Event).filter_by(id=event_id).first()
        session.close()
        return event
