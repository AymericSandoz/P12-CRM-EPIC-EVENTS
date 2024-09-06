from models import Event, Session


def get_events():
    session = Session()
    events = session.query(Event).all()
    session.close()
    return events


def get_event(event_id):
    session = Session()
    event = session.query(Event).filter_by(id=event_id).first()
    session.close()
    return event
