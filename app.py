from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data (acts as our database)
books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]

# GET /books – Retrieve all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# GET /books/<id> – Retrieve a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

# POST /books – Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "Invalid input"}), 400
    new_book = {
        "id": books[-1]["id"] + 1 if books else 1,
        "title": data["title"],
        "author": data["author"]
    }
    books.append(new_book)
    return jsonify(new_book), 201

# PUT /books/<id> – Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    book.update({
        "title": data.get("title", book["title"]),
        "author": data.get("author", book["author"])
    })
    return jsonify(book), 200

# DELETE /books/<id> – Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": f"Book {book_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
