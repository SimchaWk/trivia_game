import pytest
from services.user_service import add_user, get_user, get_users, update, delete
from models.User import User
from repository.init_database import get_db_connection


@pytest.fixture(autouse=True)
def clear_users_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM users")
        connection.commit()


def test_add_user():
    user = User(first_name="John", last_name="Doe", email="john@example.com")
    user_id = add_user(user)
    assert user_id is not None
    assert isinstance(user_id, int)


def test_get_user():
    user = User(first_name="Jane", last_name="Doe", email="jane@example.com")
    user_id = add_user(user)
    retrieved_user = get_user(user_id)
    assert retrieved_user is not None
    assert retrieved_user.first_name == "Jane"
    assert retrieved_user.last_name == "Doe"
    assert retrieved_user.email == "jane@example.com"

    non_existent_user = get_user(9999999999)
    assert non_existent_user is None


def test_get_all_users():
    user1 = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    user2 = User(first_name="Bob", last_name="Johnson", email="bob@example.com")
    add_user(user1)
    add_user(user2)
    users = get_users()
    assert len(users) == 2
    assert any(u.first_name == "Alice" for u in users)
    assert any(u.first_name == "Bob" for u in users)


def test_update_user():
    user = User(first_name="Charlie", last_name="Brown", email="charlie@example.com")
    user_id = add_user(user)
    updated_user = User(id=user_id, first_name="Charles", last_name="Brown", email="charles@example.com")
    success = update(updated_user)
    assert success is True
    retrieved_user = get_user(user_id)
    assert retrieved_user.first_name == "Charles"
    assert retrieved_user.email == "charles@example.com"


def test_delete_user():
    user = User(first_name="David", last_name="Wilson", email="david@example.com")
    user_id = add_user(user)
    success = delete(user_id)
    assert success is True
    deleted_user = get_user(user_id)
    assert deleted_user is None
