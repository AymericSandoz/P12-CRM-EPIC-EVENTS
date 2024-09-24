from models import Session, User
from utils.jwt_utils import create_jwt, decode_jwt, save_jwt, delete_jwt, load_jwt
from models import Client, Contract, Event


class AuthenticationError(Exception):
    pass


def login(email, password):
    session = Session()
    user = session.query(User).filter_by(email=email).first()

    if user and user.check_password(password):
        token = create_jwt(user.id)
        save_jwt(token)
        print("Login successful!")
        print(f"Your JWT token is: {token}")
        print("Your token will expire in 30 minutes.")
        print("Carefull, this token will be stored until you logout.")
        return token
    else:
        print("Invalid credentials.")
        raise AuthenticationError("Invalid credentials.")


def logout():
    delete_jwt()
    print("Logout successful!")


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


def check_authorization(token, action, obj_type, obj_id):
    payload = decode_jwt(token)

    if not payload:
        print("Invalid token.")
        return False

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
        return user.department.name == 'gestion' and action in ['create', 'update', 'delete']

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
        # manque vérification que le client a bien signé un contrat avec le commercial
        return True

    return False


# def check_authorization(token, action, obj_type, obj_id):
#     """
#     Vérifie si l'utilisateur a l'autorisation de réaliser une action donnée sur un type d'objet spécifique.
#     :param token: Le jeton JWT de l'utilisateur
#     :param action: L'action souhaitée (par ex: 'create', 'update', 'delete')
#     :param obj_type: Le type de l'objet ('client', 'contract', 'event')
#     :param obj_id: L'identifiant de l'objet pour valider les permissions spécifiques
#     :return: True si autorisé, sinon False
#     """
#     payload = decode_jwt(token)

#     if payload:
#         session = Session()
#         user = session.query(User).filter_by(id=payload["user_id"]).first()
#         if not user:
#             print("User not found.")
#             return False

#         print(user)

#         if not user.department:
#             print("User has no department known.")
#             return False

#         if action == 'read':
#             return True

#         elif obj_type == 'user':
#             if action in ['create', 'update', 'delete'] and user.department.name == 'gestion':
#                 return True
#             return False

#         # Vérification des permissions en fonction de l'objet et de l'action
#         if obj_type == 'client':
#             if action == 'create' and user.department.name == 'commercial':
#                 return True
#             elif action in ['update', 'delete'] and user.department.name == 'commercial':
#                 # Vérifier si le commercial est bien responsable du client
#                 client = session.query(Client).filter_by(id=obj_id).first()
#                 if client and client.commercial_id == user.id:
#                     return True
#                 else:
#                     print("Not authorized to modify this client.")
#                     return False
#             return False

#         elif obj_type == 'contract':
#             if action in ['create', 'update', 'delete'] and user.department.name == 'gestion':
#                 return True
#             elif action == 'update' and user.department.name == 'commercial':
#                 contract = session.query(Contract).filter_by(id=obj_id).first()
#                 if contract and contract.commercial_id == user.id:
#                     return True
#                 else:
#                     print("Not authorized to modify this contract.")
#                     return False

#         elif obj_type == 'event':
#             if action == 'update' and user.department.name == 'support':
#                 event = session.query(Event).filter_by(id=obj_id).first()
#                 if event and event.support_id == user.id:
#                     return True
#                 else:
#                     print("Not authorized to modify this event.")
#                     return False
#             elif action == 'assign' and user.department.name == 'gestion':
#                 return True
#             elif action == 'create' and user.department.name == 'commercial':
#                 return True

#         print("You don't have the required permissions.")
#         return False
#     return False
