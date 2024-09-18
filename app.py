from flask import Flask, jsonify, request

from api.users_api import fetch_users
from repository.init_database import create_tables_if_not_exist
from services.user_service import add_users_from_api_to_db

app = Flask(__name__)


if __name__ == '__main__':
    create_tables_if_not_exist()

    add_users_from_api_to_db(
        fetch_users()
    )

    app.run(debug=True)
