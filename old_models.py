# import argparse
# from config import SECRET_KEY, JWT_ALGORITHM
# from sqlalchemy.orm import sessionmaker
# import datetime
# import jwt
# from datetime import date
# from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, Boolean
# from sqlalchemy.orm import declarative_base, relationship, sessionmaker
# import bcrypt

# # Définir la base déclarative pour SQLAlchemy
# Base = declarative_base()


# class Department(Base):
#     __tablename__ = 'departments'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False, unique=True)

#     # Relation avec les utilisateurs
#     users = relationship('User', back_populates='department')


# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     employee_number = Column(String, unique=True, nullable=False)
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     password_hash = Column(String, nullable=False)

#     department_id = Column(Integer, ForeignKey(
#         'departments.id'), nullable=False)
#     # Relation avec le département
#     department = relationship('Department', back_populates='users')

#     # Permissions
#     can_create_clients = Column(Boolean, default=False)
#     can_modify_contracts = Column(Boolean, default=False)
#     can_assign_events = Column(Boolean, default=False)

#     def set_password(self, password):
#         # génère un sel aléatoire (saler le mot de passe). Un sel est une chaîne de caractères aléatoire qui est ajoutée au mot de passe avant le hachage.
#         salt = bcrypt.gensalt()
#         self.password_hash = bcrypt.hashpw(password.encode(
#             'utf-8'), salt)  # hachage du mot de passe avec le sel

#     def check_password(self, password):
#         # vérifie si le mot de passe est correct en comparant le hachage du mot de passe fourni avec le hachage stocké dans la base de données
#         return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)


# class Client(Base):
#     __tablename__ = 'clients'

#     id = Column(Integer, primary_key=True)
#     full_name = Column(String, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     phone = Column(String, nullable=False)
#     company_name = Column(String, nullable=False)
#     created_date = Column(Date, nullable=False)
#     last_contact_date = Column(Date)
#     contact_person = Column(String, nullable=False)

#     # Relation avec les contrats et événements
#     contracts = relationship('Contract', back_populates='client')
#     events = relationship('Event', back_populates='client')


# class Contract(Base):
#     __tablename__ = 'contracts'

#     id = Column(Integer, primary_key=True)
#     client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
#     total_amount = Column(Float, nullable=False)
#     amount_due = Column(Float, nullable=False)
#     created_date = Column(Date, nullable=False)
#     is_signed = Column(Boolean, default=False)

#     # Relation avec le client et les événements
#     client = relationship('Client', back_populates='contracts')
#     events = relationship('Event', back_populates='contract')


# class Event(Base):
#     __tablename__ = 'events'

#     id = Column(Integer, primary_key=True)
#     contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
#     client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
#     event_name = Column(String, nullable=False)
#     event_start_date = Column(Date, nullable=False)
#     event_end_date = Column(Date, nullable=False)
#     support_contact = Column(String, nullable=False)
#     location = Column(String, nullable=False)
#     attendees = Column(Integer, nullable=False)
#     notes = Column(String)

#     # Relations avec client et contrat
#     client = relationship('Client', back_populates='events')
#     contract = relationship('Contract', back_populates='events')


# # Connexion à la base de données MySQL
# DATABASE_URL = "mysql+pymysql://epicevents_user:23vttphggAymeric!@localhost/epicevents_db"

# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(engine)  # Crée les tables dans la base de données

# # Création d'une session pour interagir avec la base de données
# Session = sessionmaker(bind=engine)
# session = Session()


# # Exemple d'ajout de client
# new_client = Client(
#     full_name="John Doe",
#     email="john.doe@example.com",
#     phone="+123456789",
#     company_name="Doe Enterprises",
#     created_date=date.today(),
#     last_contact_date=date.today(),
#     contact_person="Jane Smith"
# )

# # Ajout du client à la session
# session.add(new_client)
# session.commit()

# # Exemple d'ajout de contrat
# new_contract = Contract(
#     client_id=new_client.id,
#     total_amount=5000.00,
#     amount_due=2500.00,
#     created_date=date.today(),
#     is_signed=True
# )

# # Ajout du contrat à la session
# session.add(new_contract)
# session.commit()

# # Créer un département
# management_department = Department(name="Gestion")
# session.add(management_department)
# session.commit()

# # Créer un utilisateur
# new_user = User(
#     employee_number="EMP001",
#     name="Alice Manager",
#     email="alice.manager@epicevents.com",
#     department_id=management_department.id,
#     can_create_clients=True,
#     can_modify_contracts=True,
#     can_assign_events=True
# )
# new_user.set_password("secure_password")  # Hacher et stocker le mot de passe
# session.add(new_user)
# session.commit()

# print(f"User {new_user.name} created with ID: {new_user.id}")

# # Exemple d'ajout d'événement
# new_event = Event(
#     contract_id=new_contract.id,
#     client_id=new_client.id,
#     event_name="Annual Conference",
#     event_start_date=date(2023, 10, 1),
#     event_end_date=date(2023, 10, 3),
#     support_contact="Alice Johnson",
#     location="123 Event St, Conference City",
#     attendees=200,
#     notes="Keynote at 10 AM"
# )

# # Ajout de l'événement à la session
# session.add(new_event)
# session.commit()


# def create_jwt(user_id):
#     payload = {
#         "user_id": user_id,
#         # Le jeton expire après 1 heure
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#     }
#     token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
#     return token


# def login(email, password):
#     session = Session()
#     user = session.query(User).filter_by(email=email).first()

#     if user and user.check_password(password):
#         token = create_jwt(user.id)
#         print("Login successful!")
#         print(f"Your JWT token is: {token}")
#         return token
#     else:
#         print("Invalid credentials.")
#         return None


def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None


def check_authorization(token, required_permission):
    payload = decode_jwt(token)

    if payload:
        session = Session()
        user = session.query(User).filter_by(id=payload["user_id"]).first()
        if not user:
            print("User not found.")
            return False

        # Vérifier les permissions de l'utilisateur
        if required_permission == "create_client" and user.can_create_clients:
            return True
        elif required_permission == "modify_contract" and user.can_modify_contracts:
            return True
        elif required_permission == "assign_event" and user.can_assign_events:
            return True
        else:
            print("You don't have the required permissions.")
            return False
    return False


def main():
    parser = argparse.ArgumentParser(description="Epic Events CRM CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Commande login
    login_parser = subparsers.add_parser('login')
    login_parser.add_argument('email', type=str, help='Your email')
    login_parser.add_argument('password', type=str, help='Your password')

    # Commande pour vérifier l'autorisation
    auth_parser = subparsers.add_parser('check')
    auth_parser.add_argument('token', type=str, help='Your JWT token')
    auth_parser.add_argument(
        'permission', type=str, help='The permission to check (create_client, modify_contract, assign_event)')

    args = parser.parse_args()

    if args.command == 'login':
        login(args.email, args.password)
    elif args.command == 'check':
        if check_authorization(args.token, args.permission):
            print("Action authorized.")
        else:
            print("Action not authorized.")


if __name__ == "__main__":
    main()
