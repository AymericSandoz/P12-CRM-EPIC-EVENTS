import jwt
import datetime
from config import SECRET_KEY, JWT_ALGORITHM
import os


def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=200)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None


def load_jwt():
    try:
        with open("jwt.txt", "r") as file:
            token = file.read()
            return token
    except FileNotFoundError:
        print("No JWT token found.")
        return None


def save_jwt(token):
    with open("jwt.txt", "w") as file:
        file.write(token)
        print("JWT token saved.")


def delete_jwt():
    try:
        os.remove("jwt.txt")
    except FileNotFoundError:
        print("No JWT token found.")
        return None
