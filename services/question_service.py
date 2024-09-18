from typing import Dict, Any, List
from repository.init_database import get_db_connection


def add_question(question_data: Dict[str, Any]) -> int:
    with (get_db_connection() as connection, connection.cursor() as cursor):
        cursor.execute(
            "INSERT INTO questions (question_text, correct_answer) VALUES (%s, %s) RETURNING id",
            (question_data['question'], question_data['correct_answer'])
        )
        question_id = cursor.fetchone()[0]

        for incorrect_answer in question_data['incorrect_answers']:
            cursor.execute(
                "INSERT INTO answers (question_id, incorrect_answer) VALUES (%s, %s)",
                (question_id, incorrect_answer)
            )

        connection.commit()
        return question_id


def add_multiple_questions(questions_data: List[Dict[str, Any]]) -> List[int]:
    return [add_question(question) for question in questions_data]
