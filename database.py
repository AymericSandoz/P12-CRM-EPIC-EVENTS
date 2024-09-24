import argparse
from sqlalchemy import create_engine, text
from config import DATABASE_URL
from sqlalchemy.exc import ProgrammingError

BASE_DATABASE_URL = DATABASE_URL.replace("epicevents_db", "mysql")

engine = create_engine(BASE_DATABASE_URL)

parser = argparse.ArgumentParser(
    description="Créer ou supprimer une base de données.")
parser.add_argument('action', choices=[
                    'create', 'drop'],
                    help="Action à effectuer: 'create' pour créer la base de données, 'drop' pour la supprimer.")
args = parser.parse_args()

with engine.connect() as connection:
    DB_NAME = "epicevents_db"
    try:
        if args.action == 'create':
            connection.execute(text(f"CREATE DATABASE {DB_NAME};"))
            print(f"La base de données '{DB_NAME}' a été créée avec succès.")
        elif args.action == 'drop':
            connection.execute(text(f"DROP DATABASE {DB_NAME};"))
            print(f"La base de données '{
                  DB_NAME}' a été supprimée avec succès.")
    except ProgrammingError:
        if args.action == 'create':
            print(f"La base de données '{DB_NAME}' existe déjà.")
        elif args.action == 'drop':
            print(f"La base de données '{DB_NAME}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
