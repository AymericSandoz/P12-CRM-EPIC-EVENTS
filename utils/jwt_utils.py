import jwt
import datetime
from config import SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_TIME
import os
import click


def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_TIME)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        click.echo("Token has expired. Please login again.")
        return None
    except jwt.InvalidTokenError:
        click.echo("Invalid token.")
        return None


def load_jwt():
    try:
        with open("jwt.txt", "r") as file:
            token = file.read()
            return token
    except FileNotFoundError:
        click.echo("No JWT token found.")
        return None


def save_jwt(token):
    with open("jwt.txt", "w") as file:
        file.write(token)
        click.echo("JWT token saved.")


def delete_jwt():
    try:
        os.remove("jwt.txt")
    except FileNotFoundError:
        click.echo("No JWT token found.")
        return None
