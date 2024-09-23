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

    def update(department_id, **kwargs):
        session = Session()
        department = session.query(Department).filter_by(
            id=department_id).first()
        filtered_kwargs = {key: value for key,
                           value in kwargs.items() if value is not None}
        for key, value in filtered_kwargs.items():
            setattr(department, key, value)
        session.commit()
        session.close()
        return department

    def delete(department_id):
        session = Session()
        department = session.query(Department).filter_by(
            id=department_id).first()
        session.delete(department)
        session.commit()
        session.close()
        return department
