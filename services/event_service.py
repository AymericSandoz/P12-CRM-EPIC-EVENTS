from models import Event, Session


class Event_services():
    def create(event_name, event_start_date, event_end_date, client_id, contract_id, support_contact, location, attendees, notes=None):
        session = Session()
        event = Event(
            event_name=event_name,
            contract_id=contract_id,
            client_id=client_id,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
            support_contact=support_contact,
            location=location,
            attendees=attendees,
            notes=notes
        )
        session.add(event)
        session.commit()
        event_id = event.id
        event_name = event.event_name
        session.close()
        return event_id, event_name

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

    def update(event_id, **kwargs):
        session = Session()
        event = session.query(Event).filter_by(id=event_id).first()
        filtered_kwargs = {key: value for key,
                           value in kwargs.items() if value is not None}
        for key, value in filtered_kwargs.items():
            setattr(event, key, value)
        session.commit()
        event_name = event.event_name
        session.close()
        return event_name

    def delete(event_id):
        session = Session()
        event = session.query(Event).filter_by(id=event_id).first()
        session.delete(event)
        session.commit()
        event_name = event.event_name

        session.close()
        return event_name
