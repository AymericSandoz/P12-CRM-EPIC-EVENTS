from models import Session, User
from utils.jwt_utils import create_jwt, decode_jwt, save_jwt, delete_jwt, load_jwt
from utils.args_utils import get_obj_id, get_contract_id
from models import Client, Contract, Event
from entities.entities import Commands
import sys


class AuthenticationError(Exception):
    pass


def login(email, password):
    session = Session()
    user = session.query(User).filter_by(email=email).first()

    if user and user.check_password(password):
        token = create_jwt(user.id)
        save_jwt(token)
        print(f"Your JWT token is: {token}")
        print("Your token will expire in 30 minutes.")
        print("Carefull, this token will be stored until you logout.")
        return token
    else:
        print("Invalid credentials.")
        raise AuthenticationError("Invalid credentials.")


def logout():
    delete_jwt()


def get_current_user():
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
    token = load_jwt()
    if not token:
        return False
    payload = decode_jwt(token)

    if not payload:
        return False

    action, obj_type = Commands.COMMANDS_PERMISSIONS.get(sys.argv[2])
    obj_id = get_obj_id()

    session = Session()
    user = session.query(User).filter_by(id=payload["user_id"]).first()

    if not user:
        print("User not found.")
        return False

    if not user.department:
        print("User has no department.")
        return False

    if action == 'read':
        return True

    # Check user management permissions
    if obj_type == 'user':
        if user.department.name == 'gestion' and action in ['create', 'update', 'delete']:
            return True
        else:
            print(
                "Seul le département 'gestion' peut mettre à jour, créer et supprimer des utilisateurs.")
            return False
    # Check client permissions
    if obj_type == 'client':
        return check_client_permissions(session, user, action, obj_id)

    # Check contract permissions
    if obj_type == 'contract':
        return check_contract_permissions(session, user, action, obj_id)

    # Check event permissions
    if obj_type == 'event':
        return check_event_permissions(session, user, action, obj_id)

    print("You don't have the required permissions.")
    return False


def check_client_permissions(session, user, action, client_id):
    if action == 'create' and user.department.name == 'commercial':
        return True

    if action in ['update', 'delete'] and user.department.name == 'commercial':
        client = session.query(Client).filter_by(id=client_id).first()
        if client and client.commercial_id == user.id:
            return True
        else:
            print("Not authorized to modify this client.")
            return False
    return False


def check_contract_permissions(session, user, action, contract_id):
    if action in ['create', 'update', 'delete'] and user.department.name == 'gestion':
        return True

    if action == 'update' and user.department.name == 'commercial':
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if contract and contract.commercial_id == user.id:
            return True
        else:
            print("Not authorized to modify this contract.")
            return False
    return False


def check_event_permissions(session, user, action, event_id):
    if action == 'update' and user.department.name == 'support':
        event = session.query(Event).filter_by(id=event_id).first()
        if event and event.support_id == user.id:
            return True
        else:
            print("Not authorized to modify this event.")
            return False

    if action == 'assign' and user.department.name == 'gestion':
        return True

    if action == 'create' and user.department.name == 'commercial':
        # vérification que le client a bien signé un contrat avec le commercial
        contract_id = get_contract_id()
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if contract and contract.commercial_contact_id == user.id:
            return True
        else:
            # Si le commercial n'a pas de contrat avec le client
            print("Not authorized to create an event for this client.")
            return False

    return False
