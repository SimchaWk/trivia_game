import pytest
from services import answer_service, question_service
from models import Question
from repository.init_database import get_db_connection


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


@pytest.fixture
def sample_question():
    question = Question(question_text="What is the capital of France?", correct_answer="Paris")
    question_id = question_service.add_question(question)
    return question_id


def test_add_incorrect_answers(sample_question):
    incorrect_answers = ["London", "Berlin", "Rome"]
    success = answer_service.add_incorrect_answers(sample_question, incorrect_answers)
    assert success is True

    retrieved_answers = answer_service.get_answers(sample_question)
    assert set(retrieved_answers) == set(incorrect_answers)


def test_get_incorrect_answers(sample_question):
    incorrect_answers = ["Red", "Blue", "Green"]
    answer_service.add_incorrect_answers(sample_question, incorrect_answers)

    retrieved_answers = answer_service.get_answers(sample_question)
    assert set(retrieved_answers) == set(incorrect_answers)


def test_update_incorrect_answers(sample_question):
    original_answers = ["Apple", "Banana"]
    answer_service.add_incorrect_answers(sample_question, original_answers)

    new_answers = ["Cherry", "Date", "Elderberry"]
    success = answer_service.update_answers(sample_question, new_answers)
    assert success is True

    updated_answers = answer_service.get_answers(sample_question)
    assert set(updated_answers) == set(new_answers)


def test_delete_incorrect_answers(sample_question):
    incorrect_answers = ["One", "Two", "Three"]
    answer_service.add_incorrect_answers(sample_question, incorrect_answers)

    success = answer_service.delete_answers(sample_question)
    assert success is True

    remaining_answers = answer_service.get_answers(sample_question)
    assert len(remaining_answers) == 0


def test_add_incorrect_answers_to_nonexistent_question():
    nonexistent_id = 9999999
    incorrect_answers = ["Wrong1", "Wrong2"]
    success = answer_service.add_incorrect_answers(nonexistent_id, incorrect_answers)
    assert success is False


def test_update_incorrect_answers_for_nonexistent_question():
    nonexistent_id = 9999999
    new_answers = ["New1", "New2"]
    success = answer_service.update_answers(nonexistent_id, new_answers)
    assert success is False


def test_get_answers_for_nonexistent_question():
    nonexistent_id = 9999999
    answers = answer_service.get_answers(nonexistent_id)
    assert answers == []


def test_delete_answers_for_nonexistent_question():
    nonexistent_id = 9999999
    success = answer_service.delete_answers(nonexistent_id)
    assert success is False


def test_add_empty_incorrect_answers(sample_question):
    success = answer_service.add_incorrect_answers(sample_question, [])
    assert success is True
    retrieved_answers = answer_service.get_answers(sample_question)
    assert len(retrieved_answers) == 0


def test_update_to_empty_incorrect_answers(sample_question):
    original_answers = ["Initial1", "Initial2"]
    answer_service.add_incorrect_answers(sample_question, original_answers)

    success = answer_service.update_answers(sample_question, [])
    assert success is True

    updated_answers = answer_service.get_answers(sample_question)
    assert len(updated_answers) == 0
