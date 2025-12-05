from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import os
import json
from threading import Lock
from datetime import timedelta

app = Flask(__name__)

# Secret for JWT - in production use stronger secret and don't commit it
app.config["JWT_SECRET_KEY"] = "super-secret-change-me"  # change this
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

jwt = JWTManager(app)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(DATA_DIR, "users.json")
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")
file_lock = Lock()

# Utility: load/save JSON with a lock to avoid race conditions
def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2)
        return default
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # If corrupted, overwrite with default
            with open(path, "w", encoding="utf-8") as fw:
                json.dump(default, fw, indent=2)
            return default

def save_json(path, data):
    with file_lock:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

# Initialize persistent stores (users and books)
users = load_json(USERS_FILE, {})  # { username: { "password": "<hashed>" } }
books = load_json(BOOKS_FILE, [
    {"id": 1, "title": "1984", "author": "George Orwell", "owner": "system"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "owner": "system"}
])

# ------------------------------
# Auth endpoints
# ------------------------------

@app.route("/auth/register", methods=["POST"])
def register():
    """
    Request body: { "username": "...", "password": "..." }
    """
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password required"}), 400

    username = data["username"].strip()
    password = data["password"]

    if not username or not password:
        return jsonify({"error": "username and password cannot be empty"}), 400

    if username in users:
        return jsonify({"error": "username already exists"}), 409

    hashed = generate_password_hash(password)
    users[username] = {"password": hashed}

    save_json(USERS_FILE, users)
    return jsonify({"message": "user registered", "username": username}), 201

@app.route("/auth/login", methods=["POST"])
def login():
    """
    Request body: { "username": "...", "password": "..." }
    Response: { "access_token": "..." }
    """
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password required"}), 400

    username = data["username"]
    password = data["password"]

    user = users.get(username)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200

# ------------------------------
# Book endpoints (some protected)
# ------------------------------

# GET /books – Retrieve all books (public)
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# GET /books/<id> – Retrieve a single book by ID (public)
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

# POST /books – Add a new book (requires JWT)
@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    current_user = get_jwt_identity()
    data = request.get_json()
    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_id = books[-1]["id"] + 1 if books else 1
    new_book = {
        "id": new_id,
        "title": data["title"],
        "author": data["author"],
        "owner": current_user
    }
    books.append(new_book)
    save_json(BOOKS_FILE, books)
    return jsonify(new_book), 201

# PUT /books/<id> – Update a book by ID (owner only)
@app.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Ownership check
    if book.get("owner") != current_user:
        return jsonify({"error": "forbidden: you are not the owner"}), 403

    book.update({
        "title": data.get("title", book["title"]),
        "author": data.get("author", book["author"])
    })
    save_json(BOOKS_FILE, books)
    return jsonify(book), 200

# DELETE /books/<id> – Delete a book (owner only)
@app.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    current_user = get_jwt_identity()
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Ownership check
    if book.get("owner") != current_user:
        return jsonify({"error": "forbidden: you are not the owner"}), 403

    books = [b for b in books if b["id"] != book_id]
    save_json(BOOKS_FILE, books)
    return jsonify({"message": f"Book {book_id} deleted"}), 200

# ------------------------------
# Optional: profile or other endpoints referencing authenticated user
# ------------------------------
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user = get_jwt_identity()
    # Could return more fields; currently only username exists
    return jsonify({"username": user}), 200

if __name__ == '__main__':
    # Ensure files exist initially
    save_json(USERS_FILE, users)
    save_json(BOOKS_FILE, books)
    app.run(debug=True)
