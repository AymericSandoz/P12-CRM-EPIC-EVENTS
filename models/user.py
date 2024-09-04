from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import bcrypt
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    employee_number = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(80), nullable=False)

    department_id = Column(Integer, ForeignKey(
        'departments.id'), nullable=False)
    department = relationship('Department', back_populates='users')

    can_create_clients = Column(Boolean, default=False)
    can_modify_contracts = Column(Boolean, default=False)
    can_assign_events = Column(Boolean, default=False)

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        password = password.encode('utf-8')
        return bcrypt.checkpw(password, self.password_hash.encode('utf-8'))
