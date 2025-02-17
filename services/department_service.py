from models import Session, Department
from sentry.log import log_action


def create(name):
    """Create a new department.
    Args:
        name (str): The name of the department.
    """
    session = Session()
    new_department = Department(name=name)
    session.add(new_department)
    session.commit()
    department_id = new_department.id
    department_info = {
        'name': new_department.name
    }

    new_department_name = new_department.name
    session.close()

    # Log the action
    log_action('create', 'department', obj_id=department_id,
               extra_info=department_info)

    return department_id, new_department_name


def get_all():
    """Get all departments."""
    session = Session()
    departments = session.query(Department).all()
    session.close()
    return departments


def get(department_id):
    """Get a department by id.
    Args:
        department_id (int): The id of the department to get.
    """
    session = Session()
    department = session.query(Department).filter_by(
        id=department_id).first()
    session.close()
    return department


def update(department_id, **kwargs):
    """Update a department.
    Args:
        department_id (int): The id of the department to update.
        **kwargs: The fields to update.
    """
    session = Session()
    department = session.query(Department).filter_by(
        id=department_id).first()
    if not department:
        raise ValueError("Department not found")

    filtered_kwargs = {key: value for key,
                       value in kwargs.items() if value is not None}
    for key, value in filtered_kwargs.items():
        setattr(department, key, value)
    session.commit()
    session.close()

    log_action('update', 'department', obj_id=department_id,
               extra_info=filtered_kwargs)

    return department


def delete(department_id):
    """Delete a department.
    Args:
        department_id (int): The id of the department to delete.
    """
    session = Session()
    department = session.query(Department).filter_by(
        id=department_id).first()
    if not department:
        raise ValueError("Department not found")
    department_info = {
        'name': department.name
    }
    session.delete(department)
    session.commit()
    session.close()

    # Log the action
    log_action('delete', 'department', obj_id=department_id,
               extra_info=department_info)

    return department
