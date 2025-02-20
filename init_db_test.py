# Script qui permet d'initialiser la base de données avec les départements
# et un utilisateur (l'admin par exemple) pour le département 'gestion'.
# Cet utilisateur est nécessaire pour se connecter à l'application.
# Il est créé avec le mot de passe 'mot_de_passe_admin'.
# Le mot de passe est haché avant d'être enregistré dans la base de données.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Department, User
from config import DATABASE_URL_TEST


engine = create_engine(DATABASE_URL_TEST)
Session = sessionmaker(bind=engine)
session = Session()

# Créer toutes les tables dans la base de données si elles n'existent pas
Base.metadata.create_all(engine)

# 1. Créer les départements
departments = ['commercial', 'support', 'gestion']
for dept in departments:
    existing_dept = session.query(Department).filter_by(name=dept).first()
    if not existing_dept:
        department = Department(name=dept)
        session.add(department)

# 2. Créer l'utilisateur pour le département 'gestion'
department_gestion = session.query(Department).filter_by(name='gestion').first()

# Créer l'utilisateur
new_user = User(
    employee_number='1',
    name='Chef Gestion test',
    email='admintest@gmail.com',
    department_id=department_gestion.id
)

# Hacher le mot de passe
new_user.set_password('mot_de_passe_admin')

# Ajouter l'utilisateur dans la base de données
session.add(new_user)

# Sauvegarder les changements dans la base de données
session.commit()

# Fermer la session
session.close()

print("Départements et utilisateur créés avec succès.")
