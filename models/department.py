from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    # Contrainte de vérification pour restreindre les valeurs possibles
    __table_args__ = (
        CheckConstraint(
            name.in_(['commercial', 'support', 'gestion']),
            name='check_department_name'
        ),
    )

    # Relation avec les utilisateurs
    users = relationship('User', back_populates='department')
