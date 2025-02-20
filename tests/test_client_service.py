# tests/test_client_service.py
from datetime import datetime
from services.client_service import create, get, get_all, update, delete
from models import Client, User
from unittest.mock import patch


@patch("services.client_service.get_current_user")
def test_create_client(mock_get_current_user, test_db):
    user_commercial = User(
        name="Alice Commercial",
        employee_number=999,
        email="test@hotmail.fr",
        password_hash="password123",
        department_id=2
    )
    test_db.add(user_commercial)
    test_db.commit()

    mock_get_current_user.return_value = user_commercial
    last_update_date = datetime(2025, 1, 1, 10, 30)
    client_id, full_name = create(
        full_name="John Doe",
        email="john@example.com",
        phone="+33612345678",
        company_name="JohnCorp",
        last_update=last_update_date,
    )

    assert client_id is not None
    assert full_name == "John Doe"

    test_db.commit()
    client = test_db.query(Client).filter_by(id=client_id).first()
    assert client is not None
    assert client.full_name == "John Doe"
    assert client.email == "john@example.com"
    assert client.phone == "+33612345678"
    assert client.company_name == "JohnCorp"


def test_get_client(test_db):
    """
    Teste la récupération d'un client via 'get'.
    """
    client = Client(
        full_name="Jane Roe",
        email="jane@example.com",
        phone="+33600000000",
        company_name="RoeCorp",
        last_update=datetime(2025, 2, 2, 15, 00),
        contact_person="SomeUser"
    )
    test_db.add(client)
    test_db.commit()

    fetched_client = get(client.id)
    assert fetched_client is not None
    assert fetched_client.full_name == "Jane Roe"
    assert fetched_client.email == "jane@example.com"


def test_get_all_clients(test_db):
    """
    Teste la récupération de tous les clients via 'get_all'.
    """
    c1 = Client(
        full_name="Alice",
        email="alice@example.com",
        phone="+33611111111",
        company_name="AliceCo",
        last_update=datetime(2025, 3, 3),
        contact_person="SomeUser"
    )
    c2 = Client(
        full_name="Bob",
        email="bob@example.com",
        phone="+33622222222",
        company_name="BobInc",
        last_update=datetime(2025, 4, 4),
        contact_person="SomeUser"
    )
    test_db.add(c1)
    test_db.add(c2)
    test_db.commit()

    all_clients = get_all()
    assert len(all_clients) >= 2
    names = [client.full_name for client in all_clients]
    assert "Alice" in names
    assert "Bob" in names


def test_update_client(test_db):
    """
    Teste la mise à jour d'un client via 'update'.
    """
    client = Client(
        full_name="Carl",
        email="carl@example.com",
        phone="+33677777777",
        company_name="CarlCorp",
        last_update=datetime(2025, 5, 5),
        contact_person="Old Person"
    )
    test_db.add(client)
    test_db.commit()

    updated_name = update(
        client_id=client.id,
        full_name="Carl Updated",
        email="newcarl@example.com",
        phone="+33699999999"
    )

    test_db.commit()
    assert updated_name == "Carl Updated"

    updated_client = test_db.query(Client).get(client.id)
    assert updated_client.full_name == "Carl Updated"
    assert updated_client.email == "newcarl@example.com"
    assert updated_client.phone == "+33699999999"


@patch("services.client_service.get_current_user")
def test_delete_client(mock_get_current_user, test_db):
    """
    Teste la suppression d'un client via 'delete'.
    """
    user_commercial = User(
        name="Alice Commercial",
        employee_number=999,
        email="test@hotmail.fr",
        password_hash="password123",
        department_id=2
    )
    test_db.add(user_commercial)
    test_db.commit()

    mock_get_current_user.return_value = user_commercial
    client_id, full_name = create(
        full_name="Dave",
        email="dave@example.com",
        phone="+33688888888",
        company_name="DaveCorp",
        last_update=datetime(2025, 6, 6),
    )

    deleted_name = delete(client_id)
    assert deleted_name == "Dave"

    deleted_client = test_db.query(Client).get(client_id)
    assert deleted_client is None
