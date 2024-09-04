import jwt
import datetime
from config import SECRET_KEY, JWT_ALGORITHM
from models import Session, User
from utils.jwt_utils import create_jwt, decode_jwt


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


def check_authorization(token, required_permission):
    payload = decode_jwt(token)

    if payload:
        session = Session()
        user = session.query(User).filter_by(id=payload["user_id"]).first()
        if not user:
            print("User not found.")
            return False

        if required_permission == "create_client" and user.can_create_clients:
            return True
        elif required_permission == "modify_contract" and user.can_modify_contracts:
            return True
        elif required_permission == "assign_event" and user.can_assign_events:
            return True
        else:
            print("You don't have the required permissions.")
            return False
    return False
