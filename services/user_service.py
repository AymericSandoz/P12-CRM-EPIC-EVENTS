from models import Session, User
from sentry.log import log_action


class User_Services():
    def create(employee_number, name, email, department_id, password):
        session = Session()
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
        session.close()

        # Log the action
        log_action('create', 'user', obj_id=user_id, extra_info=user_info)

        return user_id, new_user.name

    def get_all():
        session = Session()
        users = session.query(User).all()
        session.close()
        return users

    def get(user_id):
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        return user

    def update(user_id, **kwargs):
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()

        filtered_kwargs = {key: value for key,
                           value in kwargs.items() if value is not None}
        for key, value in filtered_kwargs.items():
            setattr(user, key, value)
        session.commit()
        user_info = {
            'employee_number': user.employee_number,
            'name': user.name,
            'email': user.email,
            'department_id': user.department_id,
        }
        session.close()

        # Log the action
        log_action('update', 'user', obj_id=user_id, extra_info=user_info)

        return user.name

    def delete(user_id):
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        user_info = {
            'employee_number': user.employee_number,
            'name': user.name,
            'email': user.email,
            'department_id': user.department_id
        }
        session.delete(user)
        session.commit()
        session.close()

        # Log the action
        log_action('delete', 'user', obj_id=user_id, extra_info=user_info)

        return user.name
