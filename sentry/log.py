import logging
import sentry_sdk
from services.auth import get_current_user


def log_action(action_type, obj_type, obj_id=None, extra_info=None, level='info'):
    """Journalise les actions effectuées sur des objets.

    action_type: str - Le type d'action (create, update, delete, etc.)
    obj_type: str - Le type de l'objet (user, contract, etc.)
    obj_id: int - L'ID de l'objet modifié, si applicable
    extra_info: dict - Informations supplémentaires à journaliser
    level: str - Le niveau de log ('info', 'error', etc.)
    """

    log_message = f"{action_type.capitalize()} {obj_type} (ID: {obj_id})"
    if extra_info:
        log_message += f" | Details: {extra_info}"

    user_connected = get_current_user()
    if user_connected:
        user_info = {
            'user_id': user_connected.id,
            'user_name': user_connected.name
        }
        log_message += f" | Performed by: {user_info}"

    if level == 'info':
        logging.info(log_message)
        sentry_sdk.capture_message(log_message, level='info')
    elif level == 'error':
        logging.error(log_message)
        sentry_sdk.capture_message(log_message, level='error')
