from models import Session, Department


class Department_services():
    def create(name):
        session = Session()
        new_department = Department(name=name)
        session.add(new_department)
        session.commit()
        # Accédez aux attributs avant de fermer la session
        department_id = new_department.id
        department_name = new_department.name
        session.close()
        return department_id, department_name

    def get_all():
        session = Session()
        departments = session.query(Department).all()
        session.close()
        return departments

    def get(department_id):
        session = Session()
        department = session.query(Department).filter_by(
            id=department_id).first()
        session.close()
        return department
