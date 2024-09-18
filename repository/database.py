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


if __name__ == "__main__":
    create_tables()
