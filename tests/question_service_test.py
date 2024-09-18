import pytest
from models import Question
from repository.init_database import get_db_connection
from services.question_service import *


@pytest.fixture(scope="module")
def db_connection():
    connection = get_db_connection()
    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def clear_tables(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM answers")
        cursor.execute("DELETE FROM questions")
        db_connection.commit()


def test_add_question():
    question = Question(question_text="What is the capital of France?", correct_answer="Paris")
    question_id = add_question(question)
    assert question_id is not None
    assert isinstance(question_id, int)


def test_get_question():
    question = Question(question_text="What is the largest planet in our solar system?", correct_answer="Jupiter")
    question_id = add_question(question)
    retrieved_question = get_question(question_id)
    assert retrieved_question is not None
    assert retrieved_question.question_text == question.question_text
    assert retrieved_question.correct_answer == question.correct_answer


def test_get_all_questions():
    question1 = Question(question_text="What is 2+2?", correct_answer="4")
    question2 = Question(question_text="Who wrote Hamlet?", correct_answer="William Shakespeare")
    add_question(question1)
    add_question(question2)
    questions = get_questions()
    assert len(questions) >= 2
    assert any(q.question_text == "What is 2+2?" for q in questions)
    assert any(q.question_text == "Who wrote Hamlet?" for q in questions)


def test_update_question():
    question = Question(question_text="What is the capital of Germany?", correct_answer="Berlin")
    question_id = add_question(question)
    updated_question = Question(id=question_id, question_text="What is the capital of Germany?",
                                correct_answer="Berlin (updated)")
    success = update(updated_question)
    assert success is True
    retrieved_question = get_question(question_id)
    assert retrieved_question.correct_answer == "Berlin (updated)"


def test_delete_question():
    question = Question(question_text="What is the speed of light?", correct_answer="299,792,458 m/s")
    question_id = add_question(question)
    success = delete(question_id)
    assert success is True
    deleted_question = get_question(question_id)
    assert deleted_question is None


def test_add_question_with_incorrect_answers():
    question = Question(question_text="What is the capital of Japan?", correct_answer="Tokyo")
    incorrect_answers = ["Kyoto", "Osaka", "Yokohama"]
    question_id = add_question_with_incorrect_answers(question, incorrect_answers)
    assert question_id is not None
    retrieved_question = get_question(question_id)
    assert retrieved_question is not None
    assert retrieved_question.question_text == question.question_text
