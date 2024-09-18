from flask import Flask, jsonify, request
from repository.init_database import create_tables_if_not_exist

app = Flask(__name__)


if __name__ == '__main__':
    create_tables_if_not_exist()
    app.run(debug=True)
