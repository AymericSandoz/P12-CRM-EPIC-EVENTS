from models import Session, User
from utils.jwt_utils import create_jwt, decode_jwt
from models import Client, Contract, Event


def login(email, password):
    session = Session()
    user = session.query(User).filter_by(email=email).first()

    if user and user.check_password(password):
        token = create_jwt(user.id)
        print("Login successful!")
        print(f"Your JWT token is: {token}")
        return token
    else:
        print("Invalid credentials.")
        return None


def check_authorization(token, action, obj_type, obj_id):
    """
    Vérifie si l'utilisateur a l'autorisation de réaliser une action donnée sur un type d'objet spécifique.
    :param token: Le jeton JWT de l'utilisateur
    :param action: L'action souhaitée (par ex: 'create', 'update', 'delete')
    :param obj_type: Le type de l'objet ('client', 'contract', 'event')
    :param obj_id: L'identifiant de l'objet pour valider les permissions spécifiques
    :return: True si autorisé, sinon False
    """
    payload = decode_jwt(token)

    if payload:
        session = Session()
        user = session.query(User).filter_by(id=payload["user_id"]).first()
        if not user:
            print("User not found.")
            return False

        if not user.role:
            print("User has no role.")
            return False

        # Vérification des permissions en fonction de l'objet et de l'action
        if obj_type == 'client':
            if action == 'create' and user.role == 'commercial':
                return True
            elif action in ['update', 'delete'] and user.role == 'commercial':
                # Vérifier si le commercial est bien responsable du client
                client = session.query(Client).filter_by(id=obj_id).first()
                if client and client.commercial_id == user.id:
                    return True
                else:
                    print("Not authorized to modify this client.")
                    return False

        elif obj_type == 'contract':
            if action in ['create', 'update'] and user.role == 'gestion':
                return True
            elif action == 'update' and user.role == 'commercial':
                contract = session.query(Contract).filter_by(id=obj_id).first()
                if contract and contract.commercial_id == user.id:
                    return True
                else:
                    print("Not authorized to modify this contract.")
                    return False

        elif obj_type == 'event':
            if action == 'update' and user.role == 'support':
                event = session.query(Event).filter_by(id=obj_id).first()
                if event and event.support_id == user.id:
                    return True
                else:
                    print("Not authorized to modify this event.")
                    return False
            elif action == 'assign' and user.role == 'gestion':
                return True

        print("You don't have the required permissions.")
        return False
    return False
