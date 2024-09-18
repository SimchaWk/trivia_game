from typing import List, Dict, Optional
from toolz import pipe, curry
from functools import partial
from models.User import User
from repository.init_database import get_db_connection


@curry
def add_user_to_db(connection, user: User) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id",
            (user.first_name, user.last_name, user.email)
        )
        user_id = cursor.fetchone()['id']
        connection.commit()
        return user_id


@curry
def get_user_by_id(connection, user_id: int) -> Optional[User]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, first_name, last_name, email FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        return User(
            id=result['id'], first_name=result['first_name'], last_name=result['last_name'], email=result['email']
        ) if result else None


@curry
def get_all_users(connection) -> List[User]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, first_name, last_name, email FROM users")
        return pipe(
            cursor.fetchall(),
            partial(map, lambda row: User(
                id=row['id'], first_name=row['first_name'], last_name=row['last_name'], email=row['email']
            )),
            list
        )


@curry
def update_user(connection, user: User) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE users SET first_name = %s, last_name = %s, email = %s WHERE id = %s",
            (user.first_name, user.last_name, user.email, user.id)
        )
        connection.commit()
        return cursor.rowcount > 0


@curry
def delete_user(connection, user_id: int) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()
        return cursor.rowcount > 0


def execute_db_operation(operation, *args):
    with get_db_connection() as connection:
        return operation(connection, *args)


add_user = partial(execute_db_operation, add_user_to_db)
get_user = partial(execute_db_operation, get_user_by_id)
get_users = partial(execute_db_operation, get_all_users)
update = partial(execute_db_operation, update_user)
delete = partial(execute_db_operation, delete_user)


def add_users_from_api_to_db(api_results: List[Dict]) -> List[int]:
    return pipe(
        api_results,
        partial(map, User.from_api_data),
        partial(map, add_user),
        list
    )
