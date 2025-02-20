from datetime import date
from models import Event, Client, Contract, User


def test_create_event(test_db):
    """
    Teste la création d'un Event dans la base via test_db.add(...)
    """
    user = User(
        name="Alice Commercial",
        employee_number=999,
        email="alice@email.com",
        password_hash="password123",
        department_id=1
    )
    client = Client(
        full_name="John Client",
        email="john@example.com",
        phone="+33612345678",
        company_name="JohnCorp",
        last_update=date(2025, 1, 10),
        contact_person="CommercialUser"
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
        contract_id=contract.id,
        client_id=client.id,
        event_name="My Great Event",
        event_start_date=date(2025, 2, 1),
        event_end_date=date(2025, 2, 2),
        support_contact="Support User",
        location="Paris",
        attendees=50,
        notes="Some extra details..."
    )
    test_db.add(event)
    test_db.commit()

    created_event = test_db.query(Event).get(event.id)
    assert created_event is not None
    assert created_event.event_name == "My Great Event"
    assert created_event.client_id == client.id
    assert created_event.contract_id == contract.id
    assert created_event.client_name == "John Client"
    assert "example.com" in created_event.client_contact  # f"{client.phone}, {client.email}"


def test_get_event(test_db):
    """
    Teste la récupération d'un Event : on le crée, puis on le relit
    depuis la DB pour vérifier qu'on l'obtient bien.
    """

    user = User(
        name="Commercial Bob",
        employee_number=111,
        email="bob@company.com",
        password_hash="hashedpwd",
        department_id=2
    )
    test_db.add(user)
    test_db.commit()

    client = Client(
        full_name="Jane Client",
        email="jane@example.com",
        phone="+33687654321",
        company_name="JaneCorp",
        last_update=date(2025, 3, 1),
        contact_person="CommercialUser"
    )
    test_db.add(client)
    test_db.commit()

    contract = Contract(
        client_id=client.id,
        total_amount=2000,
        commercial_contact_id=user.id,
        amount_due=1500,
    )
    test_db.add(contract)
    test_db.commit()

    event = Event(
        contract_id=contract.id,
        client_id=client.id,
        event_name="Test Get Event",
        event_start_date=date(2025, 5, 10),
        support_contact="Support X",
    )
    test_db.add(event)
    test_db.commit()

    fetched_event = test_db.query(Event).get(event.id)

    assert fetched_event is not None
    assert fetched_event.id == event.id
    assert fetched_event.event_name == "Test Get Event"
    assert fetched_event.client_id == client.id
    assert fetched_event.contract_id == contract.id
    assert fetched_event.support_contact == "Support X"
    assert fetched_event.client_name == "Jane Client"
    assert "example.com" in fetched_event.client_contact


def test_update_event(test_db):
    """
    Teste la mise à jour d'un Event existant.
    """

    user = User(
        name="Commercial Charlie",
        employee_number=222,
        email="charlie@company.com",
        password_hash="xyzpwd",
        department_id=2
    )
    test_db.add(user)
    test_db.commit()

    client = Client(
        full_name="Carl Client",
        email="carl@example.com",
        phone="+33611111111",
        company_name="CarlCorp",
        last_update=date(2025, 6, 6),
        contact_person="Carl Commercial"
    )
    test_db.add(client)
    test_db.commit()

    contract = Contract(
        client_id=client.id,
        total_amount=3000,
        commercial_contact_id=user.id,
        amount_due=3000
    )
    test_db.add(contract)
    test_db.commit()

    event = Event(
        contract_id=contract.id,
        client_id=client.id,
        event_name="Old Event Name",
        support_contact="Old Support"
    )
    test_db.add(event)
    test_db.commit()

    event.event_name = "New Event Name"
    event.support_contact = "New Support Contact"
    event.attendees = 123
    test_db.commit()

    updated_event = test_db.query(Event).get(event.id)
    assert updated_event is not None
    assert updated_event.event_name == "New Event Name"
    assert updated_event.support_contact == "New Support Contact"
    assert updated_event.attendees == 123


def test_delete_event(test_db):
    """
    Teste la suppression d'un Event.
    """

    user = User(
        name="Commercial Dave",
        employee_number=333,
        email="dave@company.com",
        password_hash="somehash",
        department_id=2
    )
    test_db.add(user)
    test_db.commit()

    client = Client(
        full_name="Dave Client",
        email="dave.client@example.com",
        phone="+33622222222",
        company_name="DaveCorp",
        last_update=date(2025, 6, 6),
        contact_person="Dave Commercial"
    )
    test_db.add(client)
    test_db.commit()

    contract = Contract(
        client_id=client.id,
        total_amount=4000,
        commercial_contact_id=user.id,
        amount_due=2000,
    )
    test_db.add(contract)
    test_db.commit()

    event = Event(
        contract_id=contract.id,
        client_id=client.id,
        event_name="Event To Delete",
        support_contact="Support Y"
    )
    test_db.add(event)
    test_db.commit()

    event_id = event.id

    test_db.delete(event)
    test_db.commit()

    deleted_event = test_db.query(Event).get(event_id)
    assert deleted_event is None
