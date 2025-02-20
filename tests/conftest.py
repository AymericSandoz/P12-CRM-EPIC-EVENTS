# conftest.py
import pytest
from models import Base, engine, Session


@pytest.fixture(scope="function")
def test_db():
    # On crée les tables avec l'engine
    Base.metadata.create_all(engine)

    # On instancie une session
    session = Session()

    yield session

    # Nettoyage
    session.rollback()
    session.close()

    # 3) Détruit les tables
    tables_to_drop = [t for t in Base.metadata.tables.values()
                      if t.name != 'departments']  # si tu veux en exclure
    Base.metadata.drop_all(engine, tables=tables_to_drop)
