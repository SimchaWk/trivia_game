from typing import List, Optional
from toolz import curry
from functools import partial
from repository.init_database import get_db_connection


@curry
def add_incorrect_answers_to_db(connection, question_id: int, incorrect_answers: List[str]) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM questions WHERE id = %s", (question_id,))
        if not cursor.fetchone():
            return False

        for answer in incorrect_answers:
            cursor.execute(
                "INSERT INTO answers (question_id, incorrect_answer) VALUES (%s, %s)",
                (question_id, answer)
            )
        connection.commit()
        return True


@curry
def get_incorrect_answers_from_db(connection, question_id: int) -> List[str]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT incorrect_answer FROM answers WHERE question_id = %s", (question_id,))
        print(cursor.fetchall())
        return [row[0] for row in cursor.fetchall()]


@curry
def update_incorrect_answers_in_db(connection, question_id: int, incorrect_answers: List[str]) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM questions WHERE id = %s", (question_id,))
        if not cursor.fetchone():
            return False

        cursor.execute("DELETE FROM answers WHERE question_id = %s", (question_id,))
        for answer in incorrect_answers:
            cursor.execute(
                "INSERT INTO answers (question_id, incorrect_answer) VALUES (%s, %s)",
                (question_id, answer)
            )
        connection.commit()
        return True


@curry
def delete_incorrect_answers_from_db(connection, question_id: int) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM answers WHERE question_id = %s", (question_id,))
        connection.commit()
        return cursor.rowcount > 0


def execute_db_operation(operation, *args):
    with get_db_connection() as connection:
        return operation(connection, *args)


add_incorrect_answers = partial(execute_db_operation, add_incorrect_answers_to_db)
get_answers = partial(execute_db_operation, get_incorrect_answers_from_db)
update_answers = partial(execute_db_operation, update_incorrect_answers_in_db)
delete_answers = partial(execute_db_operation, delete_incorrect_answers_from_db)