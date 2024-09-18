from typing import List, Dict, Optional
from toolz import pipe, curry
from functools import partial
from models import Question
from repository.init_database import get_db_connection
from services import answer_service


@curry
def add_question_to_db(connection, question: Question) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO questions (question_text, correct_answer) VALUES (%s, %s) RETURNING id",
            (question.question_text, question.correct_answer)
        )
        question_id = cursor.fetchone()['id']
        connection.commit()
        return question_id


@curry
def get_question_by_id(connection, question_id: int) -> Optional[Question]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, question_text, correct_answer FROM questions WHERE id = %s", (question_id,))
        result = cursor.fetchone()
        if result:
            return Question(
                id=result['id'], question_text=result['question_text'], correct_answer=result['correct_answer']
            )
    return None


@curry
def get_all_questions(connection) -> List[Question]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, question_text, correct_answer FROM questions")
        return [Question(id=row['id'], question_text=row['question_text'], correct_answer=row['correct_answer'])
                for row in cursor.fetchall()]


@curry
def update_question(connection, question: Question) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE questions SET question_text = %s, correct_answer = %s WHERE id = %s",
            (question.question_text, question.correct_answer, question.id)
        )
        connection.commit()
        return cursor.rowcount > 0


@curry
def delete_question(connection, question_id: int) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM questions WHERE id = %s", (question_id,))
        connection.commit()
        return cursor.rowcount > 0


def execute_db_operation(operation, *args):
    with get_db_connection() as connection:
        return operation(connection, *args)


add_question = partial(execute_db_operation, add_question_to_db)
get_question = partial(execute_db_operation, get_question_by_id)
get_questions = partial(execute_db_operation, get_all_questions)
update = partial(execute_db_operation, update_question)
delete = partial(execute_db_operation, delete_question)


def add_question_with_incorrect_answers(question: Question, incorrect_answers: List[str]) -> int:
    question_id = add_question(question)
    answer_service.add_incorrect_answers(question_id, incorrect_answers)
    return question_id


def add_questions_from_api(api_results: List[Dict]) -> List[int]:
    return pipe(
        api_results,
        partial(map, lambda data: (Question.from_api_data(data), data.get('incorrect_answers', []))),
        partial(map, lambda t: add_question_with_incorrect_answers(*t)),
        list
    )
