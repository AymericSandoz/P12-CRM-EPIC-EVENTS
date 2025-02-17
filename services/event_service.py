from models import Event, Session, User
from sentry.log import log_action
from services.auth import get_current_user


def create(event_name=None, event_start_date=None, event_end_date=None, client_id=None, contract_id=None,
           support_contact=None, location=None,
           attendees=None, notes=None):
    """Create a new event.
    Args:
        event_name (str): The name of the event.
        event_start_date (datetime): The start date of the event.
        event_end_date (datetime): The end date of the event.
        client_id (int): The id of the client.
        contract_id (int): The id of the contract.
        support_contact (str): The name of the support contact.
        location (str): The location of the event.
        attendees (str): The attendees of the event.
        notes (str): The notes of the event.
    """
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
    event_name = event.event_name
    session.close()

    # Log the action
    log_action('create', 'event', obj_id=event_id, extra_info=event_info)

    return event_id, event_name


def get_all():
    """Get all events."""
    session = Session()
    events = session.query(Event).all()
    session.close()
    return events


def get_incomplete_events(fields=None):
    """Get events with missing fields.
    Args:
        fields (list): The fields to check for missing values.
    """
    session = Session()
    query = session.query(Event)

    if fields is None:
        fields = [
            'contract_id', 'client_id', 'event_name', 'event_start_date',
            'event_end_date', 'support_contact', 'location', 'attendees', 'notes'
        ]

    filters = []
    for field in fields:
        filters.append(getattr(Event, field) is None)

    events = query.filter(*filters).all()
    session.close()
    return events


def filter_own_events():
    """Filter events where the user is the support contact."""
    session = Session()
    user = get_current_user()
    events = session.query(Event).filter_by(support_contact=user.name).all()
    session.close()
    return events


def get(event_id):
    """Get an event by id.
    Args:
        event_id (int): The id of the event to get.
    """
    session = Session()
    event = session.query(Event).filter_by(id=event_id).first()
    session.close()
    return event


def update(event_id, **kwargs):
    """Update an event.
    Args:
        event_id (int): The id of the event to update.
        **kwargs: The fields to update.
    """
    session = Session()
    event = session.query(Event).filter_by(id=event_id).first()
    if not event:
        raise ValueError("Event not found")
    filtered_kwargs = {key: value for key,
                       value in kwargs.items() if value is not None}

    for key, value in filtered_kwargs.items():
        setattr(event, key, value)

    event_name = event.event_name
    session.commit()
    session.close()

    # Log the action
    log_action('update', 'event', obj_id=event_id,
               extra_info=filtered_kwargs)

    return event_name


def assign_support_contact(event_id, support_contact):
    """Assign a support contact to an event.
    Args:
        event_id (int): The id of the event to update.
        support_contact (str): The name of the support contact.
    """
    session = Session()
    event = session.query(Event).filter_by(id=event_id).first()
    if not event:
        raise ValueError("Event not found")
        # check if the support contact exists and his department is support
    support_contact_user = session.query(User).filter_by(name=support_contact).first()
    if not support_contact_user or support_contact_user.department.name != 'support':
        raise ValueError("Support contact does not exist or is not in the support department")

    event.support_contact = support_contact
    event_name = event.event_name
    session.commit()
    session.close()

    # Log the action
    log_action('update', 'event', obj_id=event_id,
               extra_info={'support_contact': support_contact})

    return event_name


def delete(event_id):
    """Delete an event.
    Args:
        event_id (int): The id of the event to delete
    """
    session = Session()
    event = session.query(Event).filter_by(id=event_id).first()
    if not event:
        raise ValueError("Event not found")
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

    event_name = event.event_name
    session.delete(event)
    session.commit()
    session.close()

    # Log the action
    log_action('delete', 'event', obj_id=event_id, extra_info=event_info)

    return event_name
