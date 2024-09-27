# Creating a simple REST Api that allows users to manage a collection of books. 

from flask import Flask, jsonify, request, abort 

app = Flask(__name__)

# Sample data - list of books
books = [
    {'id': 1, 'title': '1984', 'author': 'George Orwell', 'rating': 4.9},
    {'id': 2, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'rating': 4.8},
]

# Helper functions to find a book by its id
def find_book(book_id):
    return next((book for book in books if book['id'] == book_id),None)

# Get /books - Return the list of all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# Get /books/<id> - Get a specific book by id
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book(book_id)
    if book:
        return jsonify(book), 200
    return abort(404, description=f"Book with id {book_id} not found")

# POST /books - Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        abort(404, description="Bad Request - Title and Author required")
        
    new_book = {
        'id': books[-1]['id'] + 1 if books else 1,
        'title': request.json['title'],
        'author': request.json['author'],
        'rating': request.json.get('rating', 0) # Default rating if not provided
    }
    books.append(new_book)
    return jsonify(new_book), 200

# PUT /books/<id> - Update a specific book by id
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = find_book(book_id)
    if not book:
        return abort(404, description=f"Book with id {book_id} not found")
    
    if not request.json:
        return abort(404, description="Bad Request - Data required to update not found")
    
    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author']) 
    book['rating'] = request.json.get('rating', book['rating'])
    
    return jsonify(book), 200

# DELETE /books/<id> - Delete a specific book by id
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        return abort(404, description=f"Book with id {book_id} not found")
    
    books.remove(book)
    return jsonify({'result' : f"Book with id: {book_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)