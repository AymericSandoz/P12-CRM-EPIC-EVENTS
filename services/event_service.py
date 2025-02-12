from models import Event, Session
from sentry.log import log_action


class Event_services():
    def create(event_name=None, event_start_date=None, event_end_date=None, client_id=None, contract_id=None,
               support_contact=None, location=None,
               attendees=None, notes=None):
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
        event_info = {
            'event_name': event.event_name,
            'contract_id': event.contract_id,
            'client_id': event.client_id,
            'event_start_date': event.event_start_date,
            'event_end_date': event.event_end_date,
            'support_contact': event.support_contact,
            'location': event.location,
            'attendees': event.attendees,
            'notes': event.notes
        }
        session.close()

        # Log the action
        log_action('create', 'event', obj_id=event_id, extra_info=event_info)

        return event_id, event.event_name

    def get_all():
        session = Session()
        events = session.query(Event).all()
        session.close()
        return events

    def get_incomplete_events(fields=None):
        """Get events with missing fields."""
        session = Session()
        query = session.query(Event)

        if fields is None:
            fields = [
                'contract_id', 'client_id', 'event_name', 'event_start_date',
                'event_end_date', 'support_contact', 'location', 'attendees', 'notes'
            ]

        filters = []
        for field in fields:
            filters.append(getattr(Event, field) == None)

        events = query.filter(*filters).all()
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
        session.close()

        # Log the action
        log_action('update', 'event', obj_id=event_id,
                   extra_info=filtered_kwargs)

        return event.event_name

    def delete(event_id):
        session = Session()
        event = session.query(Event).filter_by(id=event_id).first()
        event_info = {
            'event_name': event.event_name,
            'contract_id': event.contract_id,
            'client_id': event.client_id,
            'event_start_date': event.event_start_date,
            'event_end_date': event.event_end_date,
            'support_contact': event.support_contact,
            'location': event.location,
            'attendees': event.attendees,
            'notes': event.notes
        }
        session.delete(event)
        session.commit()
        session.close()

        # Log the action
        log_action('delete', 'event', obj_id=event_id, extra_info=event_info)

        return event.event_name
