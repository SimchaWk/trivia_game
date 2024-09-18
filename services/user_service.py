from typing import List, Dict
from toolz import pipe
from functools import partial
from models.User import User
from repository.init_database import get_db_connection


def add_user_to_db(user: User) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id",
            (user.first_name, user.last_name, user.email)
        )
        user_id = cursor.fetchone()[0]
        connection.commit()
        return user_id


def add_users_from_api_to_db(api_results: List[Dict]) -> List[int]:
    return pipe(
        api_results,
        partial(map, User.from_api_data),
        partial(map, add_user_to_db),
        list
    )
