from models import Event, Session


class Event_services():
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
