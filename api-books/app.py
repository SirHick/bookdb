import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models.book import Book

from db import db

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URI"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

@app.route("/hello", methods=["GET"])
def hello():
    return "API está funcionando!"

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()

    book = Book(
        title=data["title"],
        author=data["author"],
        description=data["description"]
    )

    db.session.add(book)
    db.session.commit()

    return jsonify({
        "message": "Livro inserido com sucesso"
    }), 201

if __name__ == "__main__":
    app.run(
        host="localhost",
        port=8086,
        debug=True
    )