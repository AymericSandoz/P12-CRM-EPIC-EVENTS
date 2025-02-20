import sys
import pytest
import services.auth
from models import User, Client, Event, Contract
from services.auth import check_authorization


@pytest.fixture
def fake_load_jwt():
    """Fixture qui simule la présence d'un token (toujours la même valeur)."""
    return "fake-token"


@pytest.fixture
def decode_jwt_ok():
    """Fixture pour decode_jwt qui renvoie un payload valide."""
    def _decode_jwt(token):
        if token == "fake-token":
            return {"user_id": 123}
        return None
    return _decode_jwt


@pytest.fixture
def decode_jwt_none():
    """Fixture pour decode_jwt qui renvoie None (token invalide)."""
    def _decode_jwt(token):
        return None
    return _decode_jwt


def test_check_authorization_gestion_create_user(
    monkeypatch,
    test_db,
    fake_load_jwt,
    decode_jwt_ok
):
    """
    Scénario A:
    - Un user du département gestion.
    - Tente de créer un user (create_user).
    - Devrait être autorisé.
    """

    monkeypatch.setattr(sys, "argv", ["main.py", "user", "create_user"])

    monkeypatch.setattr(services.auth, "load_jwt", lambda: fake_load_jwt, raising=False)
    monkeypatch.setattr(services.auth, "decode_jwt", decode_jwt_ok, raising=False)

    user = User(
        id=123,
        name="Alice Gestion",
        department_id=3,
        password_hash="xxx",
        email="alice_gestion@example.com",
        employee_number=100
    )
    test_db.add(user)
    test_db.commit()

    # 4. Appel
    authorized = check_authorization()
    assert authorized is True


def test_check_authorization_commercial_create_user_forbidden(
    monkeypatch,
    test_db,
    fake_load_jwt,
    decode_jwt_ok
):
    """
    Scénario B:
    - Un user du département commercial.
    - Tente de créer un user (create_user).
    - Devrait être refusé.
    """

    monkeypatch.setattr(sys, "argv", ["main.py", "user", "create_user"])
    monkeypatch.setattr(services.auth, "load_jwt", lambda: fake_load_jwt, raising=False)
    monkeypatch.setattr(services.auth, "decode_jwt", decode_jwt_ok, raising=False)

    user = User(
        id=123,
        name="Bob Commercial",
        department_id=1,
        password_hash="xxx",
        email="bob_commercial@example.com",
        employee_number=101
    )
    test_db.add(user)
    test_db.commit()

    authorized = check_authorization()
    assert authorized is False


def test_check_authorization_commercial_create_client(
    monkeypatch,
    test_db,
    fake_load_jwt,
    decode_jwt_ok
):
    """
    Scénario C:
    - User = commercial
    - Action = create_client
    - Devrait être autorisé.
    """

    monkeypatch.setattr(sys, "argv", ["main.py", "client", "create_client"])
    monkeypatch.setattr(services.auth, "load_jwt", lambda: fake_load_jwt, raising=False)
    monkeypatch.setattr(services.auth, "decode_jwt", decode_jwt_ok, raising=False)

    user = User(
        id=123,
        name="Bob Commercial",
        department_id=1,
        password_hash="xxx",
        email="bob_commercial@example.com",
        employee_number=101
    )
    test_db.add(user)
    test_db.commit()

    authorized = check_authorization()
    assert authorized is True


def test_check_authorization_commercial_update_client_ok(
    monkeypatch,
    test_db,
    fake_load_jwt,
    decode_jwt_ok
):
    """
    Scénario D:
    - User = support
    - Action = update_client
    - Le client lui appartient (client.contact_person == user.name)
    - Doit être autorisé.
    """
    monkeypatch.setattr(sys, "argv", ["main.py", "client", "update_client", "--obj_id", "10"])
    monkeypatch.setattr(services.auth, "load_jwt", lambda: fake_load_jwt, raising=False)
    monkeypatch.setattr(services.auth, "decode_jwt", decode_jwt_ok, raising=False)

    user = User(
        id=123,
        name="Bob Commercial",
        department_id=1,
        password_hash="xxx",
        email="bob_commercial@example.com",
        employee_number=101
    )
    test_db.add(user)
    test_db.commit()

    client = Client(
        id=10,
        full_name="Client X",
        contact_person="Bob Commercial",
        email="ttt@tt.fr",
        phone="1234567890",
        company_name="Company X",
        last_update="2021-09-01"

    )
    test_db.add(client)
    test_db.commit()

    authorized = check_authorization()
    assert authorized is True


def test_check_authorization_commercial_update_client_not_owned(
    monkeypatch,
    test_db,
    fake_load_jwt,
    decode_jwt_ok
):
    """
    Scénario E:
    - User = commercial
    - Action = update_client
    - Le client ne lui appartient pas
    - Doit être refusé.
    """
    monkeypatch.setattr(sys, "argv", ["main.py", "client", "update_client", "--obj_id", "11"])
    monkeypatch.setattr(services.auth, "load_jwt", lambda: fake_load_jwt, raising=False)
    monkeypatch.setattr(services.auth, "decode_jwt", decode_jwt_ok, raising=False)

    user = User(
        id=123,
        name="Bob Commercial",
        department_id=1,
        password_hash="xxx",
        email="bob_commercial@example.com",
        employee_number=101
    )
    test_db.add(user)
    test_db.commit()

    client = Client(
        id=11,
        full_name="Client X",
        contact_person="JEREMY TOULALAN",
        email="ttt@tt.fr",
        phone="1234567890",
        company_name="Company X",
        last_update="2021-09-01"

    )
    test_db.add(client)
    test_db.commit()

    authorized = check_authorization()
    assert authorized is False


def test_check_authorization_support_update_event_ok(
    monkeypatch,
    test_db,
    fake_load_jwt,
    decode_jwt_ok
):
    """
    Scénario F:
    - User = support
    - Action = update_event
    - L'event lui est assigné (event.support_contact == user.name)
    - Autorisé
    """
    monkeypatch.setattr(sys, "argv", ["main.py", "event", "update_event", "--obj_id", "100"])
    monkeypatch.setattr(services.auth, "load_jwt", lambda: fake_load_jwt, raising=False)
    monkeypatch.setattr(services.auth, "decode_jwt", decode_jwt_ok, raising=False)

    user = User(
        id=123,
        name="Charlie Support",
        department_id=2,
        password_hash="xxx",
        email="charlie_support@example.com",
        employee_number=102
    )
    test_db.add(user)
    test_db.commit()

    client = Client(
        id=11,
        full_name="Client X",
        contact_person="JEREMY TOULALAN",
        email="ttt@tt.fr",
        phone="1234567890",
        company_name="Company X",
        last_update="2021-09-01"

    )
    test_db.add(client)
    test_db.commit()

    contract = Contract(
        client_id=client.id,
        total_amount=1000,
        commercial_contact_id=user.id,
        amount_due=500,
    )

    test_db.add(contract)
    test_db.commit()

    event = Event(
        id=100,
        support_contact="Charlie Support",
        contract_id=contract.id,
        client_id=client.id,
        event_name="Event 1",
    )
    test_db.add(event)
    test_db.commit()

    authorized = check_authorization()
    assert authorized is True
