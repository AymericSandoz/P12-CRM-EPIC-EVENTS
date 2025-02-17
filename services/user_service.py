from models import Session, User
from sentry.log import log_action
from utils.validation_utils import validate_email


def create(employee_number, name, email, department_id, password):
    """Create a new user.
    Args:
        employee_number (int): The employee number of the user.
        name (str): The name of the user.
        email (str): The email address of the user.
        department_id (int): The id of the department.
        password (str): The password of the user
    """
    session = Session()
    if not validate_email(email):
        raise ValueError("Invalid email address")
    new_user = User(
        employee_number=employee_number,
        name=name,
        email=email,
        department_id=department_id,
    )
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    user_id = new_user.id
    user_info = {
        'employee_number': new_user.employee_number,
        'name': new_user.name,
        'email': new_user.email,
        'department_id': new_user.department_id,
    }

    new_user_name = new_user.name
    session.close()

    log_action('create', 'user', obj_id=user_id, extra_info=user_info)

    return user_id, new_user_name


def get_all():
    """Get all users."""
    session = Session()
    users = session.query(User).all()
    session.close()
    return users


def get(user_id):
    """Get a user by id.
    Args:
        user_id (int): The id of the user to get.
    """
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    return user


def update(user_id, **kwargs):
    """Update a user.
    Args:
        user_id (int): The id of the user to update.
        **kwargs: The fields to update.
    """
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise ValueError("User not found")

    filtered_kwargs = {key: value for key,
                       value in kwargs.items() if value is not None}
    if 'email' in filtered_kwargs and not validate_email(filtered_kwargs['email']):
        raise ValueError("Invalid email address")
    for key, value in filtered_kwargs.items():
        setattr(user, key, value)

    user_name = user.name
    session.commit()
    session.close()

    # Log the action
    log_action('update', 'user', obj_id=user_id,
               extra_info=filtered_kwargs)

    return user_name


def delete(user_id):
    """Delete a user.
    Args:
        user_id (int): The id of the user to delete.
    """
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise ValueError("User not found")
    user_info = {
        'employee_number': user.employee_number,
        'name': user.name,
        'email': user.email,
        'department_id': user.department_id
    }

    user_name = user.name
    session.delete(user)
    session.commit()
    session.close()

    # Log the action
    log_action('delete', 'user', obj_id=user_id, extra_info=user_info)

    return user_name
