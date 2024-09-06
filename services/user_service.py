from models import Session, User

# python create_user_script.py --employee_number 12345 --name "John Doe" --email "johndoe@example.com" --department_id 1 --password "securepassword" --can_create_clients --can_modify_contracts --can_assign_events

# Créer une classe User_Service avec get, create, etc...


class User_Service():
    def create(employee_number, name, email, department_id, password, can_create_clients=False, can_modify_contracts=False, can_assign_events=False):
        session = Session()
        new_user = User(
            employee_number=employee_number,
            name=name,
            email=email,
            department_id=department_id,
            can_create_clients=can_create_clients,
            can_modify_contracts=can_modify_contracts,
            can_assign_events=can_assign_events
        )
        new_user.set_password(password)
        session.add(new_user)
        session.commit()
        user_id = new_user.id
        user_name = new_user.name
        session.close()
        return user_id, user_name

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
