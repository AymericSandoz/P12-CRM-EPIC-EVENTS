from datetime import datetime
from models import User, Client, Contract
from services.contract_service import (
    create,
    get_all,
    get,
    update,
    delete
)


def test_create_contract(test_db):
    """
    Teste la création d'un nouveau contract via contract_service.create.
    """
    # 1) Créer un User pour le champ commercial_contact_id
    user = User(
        name="Alice Commercial",
        employee_number=101,
        email="alice@company.com",
        password_hash="pwdhash",
        department_id=2
    )
    test_db.add(user)
    test_db.commit()

    # 2) Créer un Client pour le champ client_id
    client = Client(
        full_name="John Client",
        email="john@example.com",
        phone="+33612345678",
        company_name="JohnCorp",
        last_update=datetime(2025, 1, 10),
        contact_person="Alice Commercial"
    )
    test_db.add(client)
    test_db.commit()

    # 3) Appeler la fonction create
    contract_id, returned_client_id = create(
        client_id=client.id,
        total_amount=1000.0,
        amount_due=500.0,
        commercial_contact_id=user.id,
        is_signed=False
    )

    # 4) Vérifier en base
    test_db.commit()
    created_contract = test_db.query(Contract).get(contract_id)
    assert created_contract is not None
    assert created_contract.client_id == client.id
    assert created_contract.total_amount == 1000.0
    assert created_contract.amount_due == 500.0
    assert created_contract.commercial_contact_id == user.id
    assert created_contract.is_signed is False
    # Contrôle du retour
    assert returned_client_id == client.id


def test_get_all_contracts(test_db):
    """
    Teste la récupération de tous les contrats via get_all.
    """
    # Créer 2 Users
    user1 = User(
        name="Bob Commercial",
        employee_number=102,
        email="bob@company.com",
        password_hash="bobpwd",
        department_id=2
    )
    user2 = User(
        name="Charlie Commercial",
        employee_number=103,
        email="charlie@company.com",
        password_hash="charliepwd",
        department_id=2
    )
    test_db.add_all([user1, user2])
    test_db.commit()

    # Créer 2 Clients
    client1 = Client(
        full_name="Bob Client",
        email="bob.client@example.com",
        phone="+33698765432",
        company_name="BobCorp",
        last_update=datetime(2025, 2, 15),
        contact_person="Bob Commercial"
    )
    client2 = Client(
        full_name="Charlie Client",
        email="charlie.client@example.com",
        phone="+33622222222",
        company_name="CharlieCorp",
        last_update=datetime(2025, 3, 20),
        contact_person="Charlie Commercial"
    )
    test_db.add_all([client1, client2])
    test_db.commit()

    # Créer 2 Contracts via la fonction create
    create(client1.id, 2000.0, 1000.0, user1.id, is_signed=True)
    create(client2.id, 3000.0, 500.0, user2.id, is_signed=False)

    # Appel get_all
    all_contracts = get_all()
    # On s'attend à au moins 2 contrats
    assert len(all_contracts) >= 2

    # Vérification basique
    client_ids = [c.client_id for c in all_contracts]
    assert client1.id in client_ids
    assert client2.id in client_ids


def test_get_contract(test_db):
    """
    Teste la récupération d'un contract via get.
    """
    # Créer un user + client
    user = User(
        name="Dave Commercial",
        employee_number=104,
        email="dave@company.com",
        password_hash="davepwd",
        department_id=2
    )
    test_db.add(user)
    test_db.commit()

    client = Client(
        full_name="Dave Client",
        email="dave@example.com",
        phone="+33611111111",
        company_name="DaveCorp",
        last_update=datetime(2025, 4, 10),
        contact_person="Dave Commercial"
    )
    test_db.add(client)
    test_db.commit()

    # Créer un contract
    contract_id, _ = create(
        client_id=client.id,
        total_amount=1500.0,
        amount_due=1500.0,
        commercial_contact_id=user.id,
        is_signed=False
    )

    # Appeler get
    retrieved = get(contract_id)
    assert retrieved is not None
    assert retrieved.client_id == client.id
    assert retrieved.commercial_contact_id == user.id
    assert retrieved.amount_due == 1500.0


def test_update_contract(test_db):
    """
    Teste la mise à jour d'un contract via update.
    """
    # Créer un user + client
    user = User(
        name="Frank Commercial",
        employee_number=106,
        email="frank@company.com",
        password_hash="frankpwd",
        department_id=2
    )
    test_db.add(user)
    test_db.commit()

    client = Client(
        full_name="Frank Client",
        email="frank@example.com",
        phone="+33688888888",
        company_name="FrankCorp",
        last_update=datetime(2025, 6, 10),
        contact_person="Frank Commercial"
    )
    test_db.add(client)
    test_db.commit()

    # Créer un contract
    contract_id, _ = create(
        client_id=client.id,
        total_amount=4000.0,
        amount_due=2000.0,
        commercial_contact_id=user.id,
        is_signed=False
    )

    # Mettre à jour
    updated_id = update(contract_id, amount_due=1000.0, is_signed=True)
    assert updated_id == contract_id

    # Vérifier
    test_db.commit()
    updated_contract = test_db.query(Contract).get(contract_id)
    assert updated_contract is not None
    assert updated_contract.amount_due == 1000.0
    assert updated_contract.is_signed is True


def test_delete_contract(test_db):
    """
    Teste la suppression d'un contract via delete.
    """
    # Créer un user + client
    user = User(
        name="George Commercial",
        employee_number=107,
        email="george@company.com",
        password_hash="georgepwd",
        department_id=2
    )
    test_db.add(user)
    test_db.commit()

    client = Client(
        full_name="George Client",
        email="george@example.com",
        phone="+33677777777",
        company_name="GeorgeCorp",
        last_update=datetime(2025, 7, 10),
        contact_person="George Commercial"
    )
    test_db.add(client)
    test_db.commit()

    # Créer un contract
    contract_id, _ = create(
        client_id=client.id,
        total_amount=5000.0,
        amount_due=2500.0,
        commercial_contact_id=user.id,
        is_signed=False
    )

    # Supprimer
    deleted_id = delete(contract_id)
    assert deleted_id == contract_id

    # Vérifier en base
    test_db.expire_all()
    contract_deleted = test_db.query(Contract).get(contract_id)
    assert contract_deleted is None
