import psycopg2
from psycopg2.extras import RealDictCursor
from config.sql_config import SQL_DATABASE_URI


def get_db_connection():
    return psycopg2.connect(SQL_DATABASE_URI, cursor_factory=RealDictCursor)


def create_tables():
    with (get_db_connection() as connection, connection.cursor() as cursor):

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            )
            ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                question_text VARCHAR(1000) NOT NULL,
                correct_answer VARCHAR(500) NOT NULL
            )
            ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id SERIAL PRIMARY KEY,
                question_id INTEGER REFERENCES questions(id),
                incorrect_answer VARCHAR(500) NOT NULL
            )
            ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_answers (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                question_id INTEGER REFERENCES questions(id),
                answer_text VARCHAR(500) NOT NULL,
                is_correct BOOLEAN NOT NULL,
                time_taken INTERVAL NOT NULL
            )
            ''')

    connection.commit()


def check_if_tables_exist() -> bool:
    required_tables = {'users', 'questions', 'answers', 'users_answers'}
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = ANY(%s)
        """, (list(required_tables),))
        count = cursor.fetchone()[0]
    return count == len(required_tables)


def create_tables_if_not_exist():
    if not check_if_tables_exist():
        create_tables()


def truncate_tables():
    with (get_db_connection() as connection, connection.cursor() as cursor):
        cursor.execute('''
        TRUNCATE TABLE users_answers, answers, questions, users
        RESTART IDENTITY CASCADE
        ''')


def drop_tables():
    with (get_db_connection() as connection, connection.cursor() as cursor):
        cursor.execute('''
        DROP TABLE IF EXISTS users_answers, answers, questions, users CASCADE
        ''')


if __name__ == "__main__":
    create_tables()
