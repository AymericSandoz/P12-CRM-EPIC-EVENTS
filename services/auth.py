from models import Session, User
from utils.jwt_utils import create_jwt, decode_jwt, save_jwt, delete_jwt, load_jwt
from utils.args_utils import get_obj_id, get_contract_id
from models import Client, Contract, Event
from entities.entities import Commands
import sys
from config import JWT_EXPIRATION_TIME
import click


class AuthenticationError(Exception):
    """Raised when the user is not authenticated."""
    pass


def login(email, password):
    """Login the user and return a JWT token."""
    session = Session()
    user = session.query(User).filter_by(email=email).first()

    if user and user.check_password(password):
        token = create_jwt(user.id)
        save_jwt(token)
        click.echo(f"Your JWT token is: {token}")
        click.echo(f"Your token will expire in {JWT_EXPIRATION_TIME} minutes.")
        click.echo("Carefull, this token will be stored until you logout.")
        return token
    else:
        click.echo("Invalid credentials.")
        raise AuthenticationError("Invalid credentials.")


def logout():
    """Logout the user by deleting the JWT token."""
    delete_jwt()


def get_current_user():
    """Get the current user from the JWT token.
    Returns None if the user is not authenticated."""
    token = load_jwt()
    if token:
        payload = decode_jwt(token)
        if payload:
            session = Session()
            user = session.query(User).filter_by(id=payload["user_id"]).first()
            session.close()
            return user
    return None


def check_authorization():
    """
    Check if the user has the required permissions to perform the action.
    Returns True if the user has the required permissions, False otherwise.
    User needs to be authenticated to perform any action.
    All users can read objects.(GET ALL or GET ONE)
    """
    token = load_jwt()
    if not token:
        return False
    payload = decode_jwt(token)

    if not payload:
        return False
    # sys.argv is used here to get the command path instead of click context because click context is not yet available
    action, obj_type = Commands.COMMANDS_PERMISSIONS.get(sys.argv[2])
    obj_id = get_obj_id()

    session = Session()
    user = session.query(User).filter_by(id=payload["user_id"]).first()

    if not user:
        click.echo("User not found.")
        return False

    if not user.department:
        click.echo("User has no department.")
        return False

    if action == 'read':
        return True

    # Check user management permissions
    if obj_type == 'user':
        return check_user_permissions(user, action)

    # Check client permissions
    if obj_type == 'client':
        return check_client_permissions(session, user, action, obj_id)

    # Check contract permissions
    if obj_type == 'contract':
        return check_contract_permissions(session, user, action, obj_id)

    # Check event permissions
    if obj_type == 'event':
        return check_event_permissions(session, user, action, obj_id)

    click.echo("You don't have the required permissions.")
    return False


def check_user_permissions(user, action):
    """ Check if the user has the required permissions to perform the action on a user object."""
    """ User can only be created, updated or deleted by the 'gestion' department."""
    if user.department.name == 'gestion' and action in ['create', 'update', 'delete']:
        return True
    else:
        click.echo(
            "Only users from the 'gestion' department can create, update or delete users.")
        return False


def check_client_permissions(session, user, action, client_id):
    """ Check if the user has the required permissions to perform the action on a client object.
    Commercial users can only create clients.
    Commercial users can only update or delete clients they have a contract with.
    """
    if action == 'create' and user.department.name == 'commercial':
        return True

    if action in ['update', 'delete'] and user.department.name == 'commercial':
        client = session.query(Client).filter_by(id=client_id).first()
        if client and client.contact_person == user.name:
            return True
        else:
            click.echo("Not authorized to modify this client.")
            return False
    click.echo("Not authorized to perform this action.")
    return False


def check_contract_permissions(session, user, action, contract_id):
    """ Check if the user has the required permissions to perform the action on a contract object.
    Gestion users can create, update or delete contracts any contract.
    Commercial users can only update or delete contracts where they are the commercial contact.
    Commercial users only can filter contracts where they are the commercial contact.
    """
    if action in ['create', 'update', 'delete'] and user.department.name == 'gestion':
        return True

    if action == 'update' and user.department.name == 'commercial':
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if contract and contract.commercial_id == user.id:
            return True
        else:
            click.echo("Not authorized to modify this contract.")
            return False

    if action == 'filter_contracts' and user.department.name == 'commercial':
        return True
    click.echo("Not authorized to perform this action.")
    return False


def check_event_permissions(session, user, action, event_id):
    """ Check if the user has the required permissions to perform the action on an event object.
    Support users can only update or delete events where they are the support contact.
    Commercial users can only create events for clients they have a contract with.
    Gestion users can assign a support contact to an event.
    Gestion users can filter events."
    """
    if action in ['update', 'delete'] and user.department.name == 'support':
        event = session.query(Event).filter_by(id=event_id).first()
        if event and event.support_contact == user.name:
            return True
        elif not event:
            click.echo("Event not found with this id.")
            return False
        else:
            click.echo("Not authorized to modify this event. You are not the support contact.")
            return False

    if action == 'assign_support_contact' and user.department.name == 'gestion':
        return True

    if action == 'create' and user.department.name == 'commercial':
        # vérification que le client a bien signé un contrat avec le commercial
        contract_id = get_contract_id()
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if contract and contract.commercial_contact_id == user.id:
            return True
        else:
            # Si le commercial n'a pas de contrat avec le client
            click.echo("Not authorized to create an event for this client. No contract found.")
            return False

    if action == 'filter_events' and user.department.name == 'gestion':
        return True

    if action == "filter_own_events" and user.department.name == 'support':
        return True

    click.echo("Not authorized to perform this action.")
    return False
