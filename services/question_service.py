from typing import Dict, Any, List
from models import Question
from typing import List, Dict
from toolz import pipe
from functools import partial
from repository.init_database import get_db_connection


def add_question_to_db(question: Question) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO questions (question_text, correct_answer) VALUES (%s, %s) RETURNING id",
            (question.question_text, question.correct_answer)
        )
        user_id = cursor.fetchone()[0]
        connection.commit()
        return user_id


def add_users_from_api_to_db(api_results: List[Dict]) -> List[int]:
    return pipe(
        api_results,
        partial(map, Question.from_api_data),
        partial(map, add_question_to_db),
        list
    )
