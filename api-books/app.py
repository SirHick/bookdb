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



@app.route("/books", methods=["GET"])
def listar_livros():
    livros = Book.query.all()

    return jsonify([
        livro.as_dict()
        for livro in livros
    ])

@app.route("/books/<uuid:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)

    return jsonify(book.as_dict())

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

@app.route("/books/<uuid:book_id>", methods=["PATCH"])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)

    data = request.get_json()

    for key, value in data.items():
        setattr(book, key, value)

    db.session.commit()

    return jsonify({
        "message": "Livro atualizado com sucesso"
    })


@app.route("/books/<uuid:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({
        "message": "Livro removido com sucesso"
    })

if __name__ == "__main__":
    app.run(
        host="localhost",
        port=8086,
        debug=True
    )