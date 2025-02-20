from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL, DATABASE_URL_TEST
import os
Base = declarative_base()  # classe de base pour les classes ORM

if os.environ.get("ENV") == "TEST":
    engine = create_engine(DATABASE_URL_TEST)
else:
    engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)  # créer une session pour interagir avec la base de données
