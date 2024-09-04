from models import Session, Department


def create_department(name):
    session = Session()
    new_department = Department(name=name)
    session.add(new_department)
    session.commit()
    # Accédez aux attributs avant de fermer la session
    department_id = new_department.id
    department_name = new_department.name
    session.close()
    return department_id, department_name
