from services.user_service import create, get, update, delete
from models import User


def test_create_user(test_db):
    user_id, name = create(123, "Alice", "alice@example.com", 1, "password123")

    user = test_db.query(User).filter_by(id=user_id).first()
    assert user is not None
    assert user.name == "Alice"
    assert user.email == "alice@example.com"


def test_get_user(test_db):
    user = User(employee_number=456, name="Bob", email="bob@example.com",
                department_id=2, password_hash="password123hashed")
    test_db.add(user)
    test_db.commit()

    retrieved_user = get(user.id)
    assert retrieved_user is not None
    assert retrieved_user.name == "Bob"
    assert retrieved_user.email == "bob@example.com"


def test_update_user(test_db):
    user_id, _ = create(
        employee_number=789,
        name="Charlie",
        email="charlie@example.com",
        department_id=3,
        password="secret"
    )

    updated_name = update(
        user_id=user_id,
        name="Charlie Updated",
        email="charlie.new@example.com"
    )
    assert updated_name == "Charlie Updated"

    user = test_db.query(User).get(user_id)
    assert user is not None
    assert user.name == "Charlie Updated"
    assert user.email == "charlie.new@example.com"


def test_delete_user(test_db):
    user_id, user_name = create(
        employee_number=101,
        name="Dave",
        email="dave@example.com",
        department_id=2,
        password="password123"
    )

    deleted_name = delete(user_id)
    assert deleted_name == user_name

    user = test_db.query(User).get(user_id)
    assert user is None
