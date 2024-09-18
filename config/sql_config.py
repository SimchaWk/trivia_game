import os

SQL_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost/trivia_game')
