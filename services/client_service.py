from models import Client, Session, User
from sentry.log import log_action
from utils.validation_utils import validate_email, validate_phone_number
from services.auth import get_current_user


def create(full_name, email, phone, company_name, last_update):
    """Create a new client.
    Args:
        full_name (str): The full name of the client.
        email (str): The email address of the client.
        phone (str): The phone number of the client. Expect format: +33612345678
        company_name (str): The name of the client's company.
        last_update (datetime): The date of the last update.
    """
    if not validate_email(email):
        raise ValueError("Invalid email address")
    if not validate_phone_number(phone):
        raise ValueError("Invalid phone number")
    session = Session()
    user = get_current_user()
    client = Client(
        full_name=full_name,
        email=email,
        phone=phone,
        company_name=company_name,
        last_update=last_update,
        contact_person=user.name
    )
    print("lalal", client)
    print("lalal", user.name)
    session.add(client)
    session.commit()
    client_info = {
        'full_name': client.full_name,
        'email': client.email,
        'phone': client.phone,
        'company_name': client.company_name,
        'last_update': client.last_update,
        'contact_person': client.contact_person
    }
    client_id = client.id
    session.close()
    log_action('create', 'client', obj_id=client_id,
               extra_info=client_info)
    return client_id, full_name


def get_all():
    """Get all clients."""
    session = Session()
    clients = session.query(Client).all()
    session.close()
    return clients


def get(client_id):
    """Get a client by id.
    Args:
        client_id (int): The id of the client to get.
    """
    session = Session()
    client = session.query(Client).filter_by(id=client_id).first()
    session.close()
    return client


def update(client_id, **kwargs):
    """Update a client.
    Args:
        client_id (int): The id of the client to update.
        **kwargs: The fields to update.
    """
    session = Session()
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        raise ValueError("Client not found")
    # Filtrer les champs non nuls
    filtered_kwargs = {key: value for key,
                       value in kwargs.items() if value is not None}

    if 'email' in filtered_kwargs and not validate_email(filtered_kwargs['email']):
        raise ValueError("Invalid email address")
    if 'phone' in filtered_kwargs and not validate_phone_number(filtered_kwargs['phone']):
        raise ValueError("Invalid phone number")
    if 'contact_person' in filtered_kwargs:
        user = session.query(User).filter_by(
            name=filtered_kwargs['contact_person']
        ).filter(User.department.has(name='commercial')).first()
        if not user:
            raise ValueError("Contact person must be a user from the commercial department")
    for key, value in filtered_kwargs.items():
        setattr(client, key, value)

    client_name = client.full_name
    session.commit()

    session.close()
    log_action('update', 'client', obj_id=client_id,
               extra_info=filtered_kwargs)
    return client_name


def delete(client_id):
    """Delete a client.
    Args:
        client_id (int): The id of the client to delete.
    """
    session = Session()
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        raise ValueError("Client not found")
    client_name = client.full_name
    session.delete(client)
    session.commit()
    client_info = {
        'full_name': client.full_name,
        'email': client.email,
        'phone': client.phone,
        'company_name': client.company_name,
        'last_update': client.last_update,
        'contact_person': client.contact_person
    }
    session.close()

    log_action('delete', 'client', obj_id=client_id,
               extra_info=client_info)
    return client_name
